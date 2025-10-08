"""
Alert Engine for monitoring dork results and triggering notifications.
"""

from django.utils import timezone
from django.db.models import Q, Count
from typing import List, Dict, Optional
import logging

from ..models_automation import Alert, AlertHistory, AutomatedDork
from ..models import SearchResult
from .email_service import EmailService

logger = logging.getLogger(__name__)


class AlertEngine:
    """
    Service for evaluating alert conditions and triggering notifications.
    """
    
    @staticmethod
    def check_and_trigger_alerts(dork_id: int, new_results: List[SearchResult]) -> List[AlertHistory]:
        """
        Check all active alerts for a dork and trigger if conditions are met.
        
        Args:
            dork_id: ID of the dork that was executed
            new_results: List of new SearchResult objects found
            
        Returns:
            List of AlertHistory objects created
        """
        from ..models import GoogleDork
        
        triggered_alerts = []
        
        try:
            dork = GoogleDork.objects.get(id=dork_id)
            active_alerts = Alert.objects.filter(
                dork=dork,
                is_active=True
            )
            
            for alert in active_alerts:
                should_trigger = AlertEngine._evaluate_alert_condition(
                    alert,
                    dork,
                    new_results
                )
                
                if should_trigger:
                    alert_history = AlertEngine._trigger_alert(
                        alert,
                        new_results
                    )
                    if alert_history:
                        triggered_alerts.append(alert_history)
            
            return triggered_alerts
            
        except Exception as e:
            logger.error(f"Error checking alerts for dork {dork_id}: {str(e)}")
            return []
    
    @staticmethod
    def _evaluate_alert_condition(
        alert: Alert,
        dork,
        new_results: List[SearchResult]
    ) -> bool:
        """
        Evaluate whether an alert condition is met.
        
        Args:
            alert: Alert object to evaluate
            dork: GoogleDork object
            new_results: List of new results
            
        Returns:
            bool: True if alert should be triggered
        """
        trigger_type = alert.trigger_type
        
        if trigger_type == 'new_results':
            # Trigger if any new results found
            return len(new_results) > 0
        
        elif trigger_type == 'result_count_change':
            # Trigger if result count changed significantly
            threshold = alert.condition_data.get('threshold', 5)
            return len(new_results) >= threshold
        
        elif trigger_type == 'keyword_found':
            # Trigger if specific keywords found in results
            keywords = alert.condition_data.get('keywords', [])
            if not keywords:
                return False
            
            keywords_lower = [k.lower() for k in keywords]
            for result in new_results:
                result_text = f"{result.title} {result.snippet}".lower()
                if any(keyword in result_text for keyword in keywords_lower):
                    return True
            return False
        
        elif trigger_type == 'scheduled_report':
            # Check if it's time for scheduled report
            # This would typically be triggered by a cron job
            return True
        
        return False
    
    @staticmethod
    def _trigger_alert(
        alert: Alert,
        new_results: List[SearchResult]
    ) -> Optional[AlertHistory]:
        """
        Trigger an alert and send notifications.
        
        Args:
            alert: Alert to trigger
            new_results: New results that triggered the alert
            
        Returns:
            AlertHistory object if successful, None otherwise
        """
        try:
            # Create alert history record
            alert_history = AlertHistory.objects.create(
                alert=alert,
                result_count=len(new_results),
                new_results_count=len(new_results),
                result_summary=AlertEngine._create_result_summary(new_results),
                notification_sent=False
            )
            
            # Send email notification if enabled
            if alert.send_email:
                recipients = alert.get_recipient_list()
                
                # Prepare results preview
                results_preview = [
                    {
                        'title': result.title,
                        'url': result.url,
                        'snippet': result.snippet[:200] if result.snippet else ''
                    }
                    for result in new_results[:10]  # Top 10 results
                ]
                
                # Send notification email
                success = EmailService.send_new_results_notification(
                    alert_name=alert.name,
                    dork_query=alert.dork.query,
                    new_results_count=len(new_results),
                    total_results=SearchResult.objects.filter(dork=alert.dork).count(),
                    results_preview=results_preview,
                    recipients=recipients,
                    dork_id=alert.dork.id
                )
                
                # Update notification status
                alert_history.notification_sent = success
                alert_history.notification_details = {
                    'success': success,
                    'recipients': recipients,
                    'sent_at': timezone.now().isoformat()
                }
                alert_history.save()
                
                logger.info(f"Alert '{alert.name}' triggered successfully. Email sent: {success}")
            
            # Update alert metadata
            alert.last_triggered = timezone.now()
            alert.trigger_count += 1
            alert.save()
            
            return alert_history
            
        except Exception as e:
            logger.error(f"Error triggering alert {alert.id}: {str(e)}")
            return None
    
    @staticmethod
    def _create_result_summary(results: List[SearchResult]) -> str:
        """
        Create a text summary of search results.
        
        Args:
            results: List of SearchResult objects
            
        Returns:
            str: Summary text
        """
        if not results:
            return "No results found"
        
        summary_lines = []
        for i, result in enumerate(results[:5], 1):
            summary_lines.append(f"{i}. {result.title[:100]}")
            summary_lines.append(f"   URL: {result.url}")
            if result.snippet:
                summary_lines.append(f"   Snippet: {result.snippet[:150]}...")
            summary_lines.append("")
        
        if len(results) > 5:
            summary_lines.append(f"... and {len(results) - 5} more results")
        
        return "\n".join(summary_lines)
    
    @staticmethod
    def run_automated_dorks() -> Dict:
        """
        Execute all automated dorks that are due to run.
        This should be called by a scheduled task (e.g., Celery beat).
        
        Returns:
            Dict with execution summary
        """
        now = timezone.now()
        
        # Find all active automations that are due to run
        due_automations = AutomatedDork.objects.filter(
            is_active=True,
            next_run__lte=now
        ).select_related('dork', 'created_by')
        
        results = {
            'total': due_automations.count(),
            'successful': 0,
            'failed': 0,
            'details': []
        }
        
        for automation in due_automations:
            try:
                # Execute the dork
                # Note: This would integrate with your existing dork execution logic
                execution_result = AlertEngine._execute_automated_dork(automation)
                
                if execution_result['success']:
                    results['successful'] += 1
                else:
                    results['failed'] += 1
                
                results['details'].append({
                    'automation_id': automation.id,
                    'dork_query': automation.dork.query,
                    'status': 'success' if execution_result['success'] else 'failed',
                    'result_count': execution_result.get('result_count', 0),
                    'execution_time': execution_result.get('execution_time', 0)
                })
                
            except Exception as e:
                logger.error(f"Failed to execute automation {automation.id}: {str(e)}")
                results['failed'] += 1
                results['details'].append({
                    'automation_id': automation.id,
                    'status': 'failed',
                    'error': str(e)
                })
        
        return results
    
    @staticmethod
    def _execute_automated_dork(automation: AutomatedDork) -> Dict:
        """
        Execute a single automated dork.
        
        Args:
            automation: AutomatedDork object to execute
            
        Returns:
            Dict with execution results
        """
        import time
        start_time = time.time()
        
        try:
            # This is a placeholder - integrate with your actual dork execution logic
            # For now, we'll just mark it as run
            
            result_count = 0  # Would be actual result count from execution
            errors = []
            
            # Mark automation as run
            automation.mark_as_run(result_count=result_count)
            
            # Send completion email if enabled
            if automation.send_email_on_completion:
                recipients = [
                    email.strip()
                    for email in automation.email_recipients.split(',')
                    if email.strip()
                ] or [automation.created_by.email]
                
                execution_time = time.time() - start_time
                
                EmailService.send_automation_complete(
                    automation_name=f"Automated: {automation.dork.title}",
                    dork_query=automation.dork.query,
                    result_count=result_count,
                    execution_time=execution_time,
                    recipients=recipients,
                    errors=errors if errors else None
                )
            
            return {
                'success': True,
                'result_count': result_count,
                'execution_time': time.time() - start_time
            }
            
        except Exception as e:
            logger.error(f"Error executing automated dork {automation.id}: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'execution_time': time.time() - start_time
            }

import React, { useCallback, useEffect, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import ReactFlow, {
    Controls,
    Background,
    useNodesState,
    useEdgesState,
    Panel,
    MiniMap,
    ConnectionLineType,
    MarkerType,
    type Node,
    type Edge,
    type NodeTypes,
    type Connection,
    addEdge,
} from 'reactflow';
import 'reactflow/dist/style.css';
import { entitiesService } from '../services/entitiesService';
import type { Entity, EntityRelationship } from '../types';
import { useNavigate } from 'react-router-dom';

interface EnhancedRelationshipGraphProps {
    entity: Entity;
}

// Enhanced custom node component with tooltips and animations
const EnhancedEntityNode = ({ data }: { data: { label: string; entityId?: string; isCurrent?: boolean; entityType?: string; priority?: string; status?: string; icon?: string; relationshipCount?: number } }) => {
    const navigate = useNavigate();
    const [showTooltip, setShowTooltip] = useState(false);

    const handleClick = () => {
        if (data.entityId && !data.isCurrent) {
            navigate(`/entities/${data.entityId}`);
        }
    };

    return (
        <div className="relative">
            <div
                onClick={handleClick}
                onMouseEnter={() => setShowTooltip(true)}
                onMouseLeave={() => setShowTooltip(false)}
                className={`px-4 py-3 rounded-lg border-2 shadow-lg transition-all transform hover:scale-105 ${data.isCurrent
                    ? 'bg-gradient-to-br from-blue-500 to-blue-600 text-white border-blue-700 shadow-blue-300'
                    : 'bg-white text-gray-900 border-gray-300 hover:border-blue-400 hover:shadow-2xl cursor-pointer hover:-translate-y-1'
                    }`}
                style={{ minWidth: '180px' }}
            >
                <div className="flex items-center gap-2">
                    <div className="text-2xl">{data.icon || '🔷'}</div>
                    <div className="flex-1">
                        <div className="font-bold text-sm">{data.label}</div>
                        {data.entityType && (
                            <div className={`text-xs ${data.isCurrent ? 'text-blue-100' : 'text-gray-500'}`}>
                                {data.entityType}
                            </div>
                        )}
                    </div>
                </div>
                {data.relationshipCount !== undefined && (
                    <div className={`text-xs mt-2 flex items-center gap-1 ${data.isCurrent ? 'text-blue-100' : 'text-gray-500'}`}>
                        <span>🔗</span>
                        {data.relationshipCount} connection{data.relationshipCount !== 1 ? 's' : ''}
                    </div>
                )}
            </div>

            {/* Enhanced Tooltip */}
            {showTooltip && !data.isCurrent && (
                <div className="absolute z-50 top-full mt-2 left-1/2 transform -translate-x-1/2 bg-gray-900 text-white text-xs rounded-lg p-3 shadow-xl whitespace-nowrap animate-fadeIn">
                    <div className="font-semibold mb-1">{data.label}</div>
                    {data.entityType && <div className="text-gray-300">Type: {data.entityType}</div>}
                    {data.relationshipCount !== undefined && data.relationshipCount > 0 && (
                        <div className="text-gray-300">{data.relationshipCount} relationship{data.relationshipCount !== 1 ? 's' : ''}</div>
                    )}
                    <div className="text-blue-300 mt-1">Click to view →</div>
                    {/* Arrow */}
                    <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-4 border-r-4 border-b-4 border-transparent border-b-gray-900"></div>
                </div>
            )}
        </div>
    );
};

const nodeTypes: NodeTypes = {
    entity: EnhancedEntityNode,
};

// Enhanced layout algorithms
type LayoutType = 'circular' | 'force' | 'hierarchical' | 'grid';

const calculateLayout = (
    centerEntity: Entity,
    outgoing: EntityRelationship[],
    incoming: EntityRelationship[],
    layoutType: LayoutType = 'circular'
): { nodes: Node[]; edges: Edge[] } => {
    const nodes: Node[] = [];
    const edges: Edge[] = [];
    const entityMap = new Map<number, { name: string; type: string; icon?: string }>();

    // Add center node
    nodes.push({
        id: `entity-${centerEntity.id}`,
        type: 'entity',
        position: { x: 500, y: 350 },
        data: {
            label: centerEntity.name,
            entityType: centerEntity.entity_type_name,
            entityId: centerEntity.id,
            icon: centerEntity.entity_type_data?.icon,
            isCurrent: true,
            relationshipCount: outgoing.length + incoming.length,
        },
    });

    // Collect all related entities
    outgoing.forEach((rel) => {
        entityMap.set(rel.to_entity, {
            name: rel.to_entity_name,
            type: 'Connected Entity',
        });
    });

    incoming.forEach((rel) => {
        entityMap.set(rel.from_entity, {
            name: rel.from_entity_name,
            type: 'Connected Entity',
        });
    });

    const relatedEntities = Array.from(entityMap.entries());

    // Apply different layout algorithms
    switch (layoutType) {
        case 'circular': {
            const radius = 350;
            const angleStep = (2 * Math.PI) / relatedEntities.length;

            relatedEntities.forEach(([entityId, info], index) => {
                const angle = index * angleStep;
                const x = 500 + radius * Math.cos(angle);
                const y = 350 + radius * Math.sin(angle);

                nodes.push({
                    id: `entity-${entityId}`,
                    type: 'entity',
                    position: { x, y },
                    data: {
                        label: info.name,
                        entityType: info.type,
                        entityId: entityId,
                        icon: info.icon,
                        isCurrent: false,
                    },
                });
            });
            break;
        }

        case 'grid': {
            const cols = Math.ceil(Math.sqrt(relatedEntities.length));
            const spacing = 250;

            relatedEntities.forEach(([entityId, info], index) => {
                const row = Math.floor(index / cols);
                const col = index % cols;
                const x = 200 + col * spacing;
                const y = 100 + row * spacing;

                nodes.push({
                    id: `entity-${entityId}`,
                    type: 'entity',
                    position: { x, y },
                    data: {
                        label: info.name,
                        entityType: info.type,
                        entityId: entityId,
                        icon: info.icon,
                        isCurrent: false,
                    },
                });
            });
            break;
        }

        case 'hierarchical': {
            const outgoingEntities = outgoing.map(rel => rel.to_entity);
            const spacing = 250;

            // Outgoing on the right
            outgoing.forEach((rel, index) => {
                nodes.push({
                    id: `entity-${rel.to_entity}`,
                    type: 'entity',
                    position: { x: 800, y: 150 + index * spacing },
                    data: {
                        label: rel.to_entity_name,
                        entityType: 'Connected',
                        entityId: rel.to_entity,
                        isCurrent: false,
                    },
                });
            });

            // Incoming on the left
            incoming.forEach((rel, index) => {
                if (!outgoingEntities.includes(rel.from_entity)) {
                    nodes.push({
                        id: `entity-${rel.from_entity}`,
                        type: 'entity',
                        position: { x: 200, y: 150 + index * spacing },
                        data: {
                            label: rel.from_entity_name,
                            entityType: 'Connected',
                            entityId: rel.from_entity,
                            isCurrent: false,
                        },
                    });
                }
            });
            break;
        }

        default:
            // Circular layout as default
            break;
    }

    // Add edges with enhanced styling
    outgoing.forEach((rel) => {
        const confidence = rel.confidence || rel.strength / 10;
        const strengthColor = confidence >= 0.8 ? '#ef4444' : confidence >= 0.5 ? '#f59e0b' : '#10b981';

        edges.push({
            id: `edge-out-${rel.id}`,
            source: `entity-${centerEntity.id}`,
            target: `entity-${rel.to_entity}`,
            type: 'smoothstep',
            animated: confidence >= 0.8,
            style: {
                stroke: strengthColor,
                strokeWidth: Math.max(2, confidence * 5),
            },
            markerEnd: {
                type: MarkerType.ArrowClosed,
                color: strengthColor,
                width: 20,
                height: 20,
            },
            label: rel.relationship_type.replace('_', ' '),
            labelStyle: {
                fill: '#1f2937',
                fontSize: 12,
                fontWeight: 600,
            },
            labelBgStyle: {
                fill: '#ffffff',
                fillOpacity: 0.95,
            },
            data: {
                relationship: rel,
            },
        });
    });

    incoming.forEach((rel) => {
        const confidence = rel.confidence || rel.strength / 10;
        const strengthColor = confidence >= 0.8 ? '#ef4444' : confidence >= 0.5 ? '#f59e0b' : '#10b981';

        edges.push({
            id: `edge-in-${rel.id}`,
            source: `entity-${rel.from_entity}`,
            target: `entity-${centerEntity.id}`,
            type: 'smoothstep',
            animated: confidence >= 0.8,
            style: {
                stroke: strengthColor,
                strokeWidth: Math.max(2, confidence * 5),
            },
            markerEnd: {
                type: MarkerType.ArrowClosed,
                color: strengthColor,
                width: 20,
                height: 20,
            },
            label: rel.relationship_type.replace('_', ' '),
            labelStyle: {
                fill: '#1f2937',
                fontSize: 12,
                fontWeight: 600,
            },
            labelBgStyle: {
                fill: '#ffffff',
                fillOpacity: 0.95,
            },
            data: {
                relationship: rel,
            },
        });
    });

    return { nodes, edges };
};

const EnhancedRelationshipGraph: React.FC<EnhancedRelationshipGraphProps> = ({ entity }) => {
    const [nodes, setNodes, onNodesChange] = useNodesState([]);
    const [edges, setEdges, onEdgesChange] = useEdgesState([]);
    const [layoutType, setLayoutType] = useState<LayoutType>('circular');
    const [selectedRelationshipType, setSelectedRelationshipType] = useState<string>('all');
    const [showLabels, setShowLabels] = useState(true);

    // Fetch relationships
    const { data: relationships, isLoading, error } = useQuery({
        queryKey: ['entity-relationships', entity.id],
        queryFn: () => entitiesService.getEntityRelationships(entity.id),
    });

    // Update graph when relationships or filters change
    useEffect(() => {
        if (relationships) {
            let outgoing = relationships.outgoing;
            let incoming = relationships.incoming;

            // Filter by relationship type
            if (selectedRelationshipType !== 'all') {
                outgoing = outgoing.filter(rel => rel.relationship_type === selectedRelationshipType);
                incoming = incoming.filter(rel => rel.relationship_type === selectedRelationshipType);
            }

            const { nodes: newNodes, edges: newEdges } = calculateLayout(
                entity,
                outgoing,
                incoming,
                layoutType
            );

            // Hide labels if disabled
            if (!showLabels) {
                newEdges.forEach(edge => {
                    edge.label = undefined;
                });
            }

            setNodes(newNodes);
            setEdges(newEdges);
        }
    }, [relationships, entity, layoutType, selectedRelationshipType, showLabels, setNodes, setEdges]);

    const onConnect = useCallback(
        (params: Connection) => setEdges((eds) => addEdge(params, eds)),
        [setEdges]
    );

    const onNodeClick = useCallback((_: React.MouseEvent, node: Node) => {
        console.log('Selected node:', node.id, node.data);
    }, []);

    // Export graph as PNG
    const exportGraph = () => {
        const graphElement = document.querySelector('.react-flow') as HTMLElement;
        if (graphElement) {
            // Use html2canvas or similar library for real export
            alert('Export feature - Install html2canvas library for actual implementation');
        }
    };

    // Get unique relationship types
    const relationshipTypes = React.useMemo(() => {
        if (!relationships) return [];
        const types = new Set<string>();
        relationships.outgoing.forEach(rel => types.add(rel.relationship_type));
        relationships.incoming.forEach(rel => types.add(rel.relationship_type));
        return Array.from(types);
    }, [relationships]);

    if (isLoading) {
        return (
            <div className="flex items-center justify-center h-96">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-blue-500 mx-auto mb-4"></div>
                    <p className="text-gray-600 font-medium">Loading enhanced relationship graph...</p>
                    <p className="text-gray-400 text-sm mt-2">Preparing interactive visualization...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="text-center py-12 bg-red-50 rounded-lg border-2 border-red-200">
                <div className="text-red-500 text-6xl mb-4">⚠️</div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">
                    Error Loading Graph
                </h3>
                <p className="text-gray-600 mb-4">
                    Failed to load relationship data. Please try again.
                </p>
                <button
                    onClick={() => window.location.reload()}
                    className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
                >
                    Retry
                </button>
            </div>
        );
    }

    const totalRelationships = (relationships?.outgoing.length || 0) + (relationships?.incoming.length || 0);

    if (totalRelationships === 0) {
        return (
            <div className="text-center py-16 bg-gradient-to-br from-gray-50 to-gray-100 rounded-lg border-2 border-dashed border-gray-300">
                <div className="text-gray-300 text-7xl mb-4">🔗</div>
                <h3 className="text-2xl font-bold text-gray-900 mb-3">
                    No Relationships Found
                </h3>
                <p className="text-gray-600 mb-4 max-w-md mx-auto">
                    This entity doesn't have any relationships yet. Start building your network by adding connections!
                </p>
                <p className="text-sm text-gray-500 mb-6">
                    Go to the <strong>"Relationships"</strong> tab to add new connections.
                </p>
                <div className="flex justify-center gap-2">
                    <span className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-xs font-medium">
                        💡 Tip: Map business relationships
                    </span>
                    <span className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-xs font-medium">
                        🎯 Track connections
                    </span>
                </div>
            </div>
        );
    }

    return (
        <div className="space-y-4">
            {/* Enhanced Control Panel */}
            <div className="bg-white rounded-lg border border-gray-200 p-4 shadow-sm">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {/* Layout Selector */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            📐 Layout Algorithm
                        </label>
                        <select
                            value={layoutType}
                            onChange={(e) => setLayoutType(e.target.value as LayoutType)}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                            <option value="circular">🔵 Circular</option>
                            <option value="hierarchical">📊 Hierarchical</option>
                            <option value="grid">⊞ Grid</option>
                        </select>
                    </div>

                    {/* Relationship Type Filter */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            🔍 Filter by Type
                        </label>
                        <select
                            value={selectedRelationshipType}
                            onChange={(e) => setSelectedRelationshipType(e.target.value)}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                            <option value="all">All Types ({totalRelationships})</option>
                            {relationshipTypes.map(type => (
                                <option key={type} value={type}>
                                    {type.replace('_', ' ')}
                                </option>
                            ))}
                        </select>
                    </div>

                    {/* View Options */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            ⚙️ View Options
                        </label>
                        <div className="space-y-2">
                            <label className="flex items-center gap-2 cursor-pointer">
                                <input
                                    type="checkbox"
                                    checked={showLabels}
                                    onChange={(e) => setShowLabels(e.target.checked)}
                                    className="w-4 h-4 text-blue-600 rounded focus:ring-2 focus:ring-blue-500"
                                />
                                <span className="text-sm text-gray-700">Show edge labels</span>
                            </label>
                            <button
                                onClick={exportGraph}
                                className="w-full px-3 py-1.5 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors text-sm font-medium"
                            >
                                📥 Export Graph
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            {/* Enhanced Graph Container */}
            <div className="h-[700px] bg-gradient-to-br from-gray-50 to-gray-100 rounded-lg border-2 border-gray-200 shadow-lg relative overflow-hidden">
                <ReactFlow
                    nodes={nodes}
                    edges={edges}
                    onNodesChange={onNodesChange}
                    onEdgesChange={onEdgesChange}
                    onConnect={onConnect}
                    onNodeClick={onNodeClick}
                    nodeTypes={nodeTypes}
                    connectionLineType={ConnectionLineType.SmoothStep}
                    fitView
                    attributionPosition="bottom-left"
                    className="bg-gradient-to-br from-gray-50 to-gray-100"
                    minZoom={0.2}
                    maxZoom={4}
                    defaultViewport={{ x: 0, y: 0, zoom: 0.8 }}
                >
                    <Background
                        color="#cbd5e1"
                        gap={20}
                        size={1}
                    />
                    <Controls showInteractive={false} />
                    <MiniMap
                        nodeColor={(node) => {
                            if (node.data.isCurrent) return '#3b82f6';
                            return '#94a3b8';
                        }}
                        maskColor="rgba(0, 0, 0, 0.1)"
                        className="!bg-white !border-2 !border-gray-300 !rounded-lg"
                    />

                    {/* Enhanced Info Panel */}
                    <Panel position="top-left" className="bg-white/95 backdrop-blur rounded-xl shadow-2xl p-4 border-2 border-gray-200">
                        <h3 className="font-bold text-gray-900 mb-3 flex items-center gap-2">
                            <span className="text-xl">🕸️</span>
                            Relationship Network
                        </h3>
                        <div className="space-y-2 text-sm text-gray-600">
                            <div className="flex items-center gap-2">
                                <div className="w-4 h-4 bg-gradient-to-br from-blue-500 to-blue-600 rounded shadow-sm"></div>
                                <span className="font-medium">Current Entity</span>
                            </div>
                            <div className="flex items-center gap-2">
                                <div className="w-4 h-4 bg-white border-2 border-gray-300 rounded shadow-sm"></div>
                                <span>Related Entities</span>
                            </div>
                            <div className="pt-2 border-t border-gray-200 mt-2">
                                <div className="text-xs font-semibold text-gray-700 mb-2">Connection Strength:</div>
                                <div className="space-y-1.5">
                                    <div className="flex items-center gap-2">
                                        <div className="w-10 h-1 bg-green-500 rounded"></div>
                                        <span className="text-xs">Low (0-50%)</span>
                                    </div>
                                    <div className="flex items-center gap-2">
                                        <div className="w-10 h-1.5 bg-amber-500 rounded"></div>
                                        <span className="text-xs">Medium (50-80%)</span>
                                    </div>
                                    <div className="flex items-center gap-2">
                                        <div className="w-10 h-2 bg-red-500 rounded animate-pulse"></div>
                                        <span className="text-xs">High (80-100%)</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </Panel>

                    {/* Enhanced Stats Panel */}
                    <Panel position="top-right" className="bg-white/95 backdrop-blur rounded-xl shadow-2xl p-4 border-2 border-gray-200">
                        <h4 className="font-bold text-gray-900 mb-3 flex items-center gap-2">
                            <span className="text-xl">📊</span>
                            Network Stats
                        </h4>
                        <div className="space-y-3 text-sm">
                            <div className="bg-gray-50 rounded-lg p-2">
                                <span className="text-gray-600">Total Connections</span>
                                <div className="text-2xl font-bold text-gray-900">{totalRelationships}</div>
                            </div>
                            <div className="bg-blue-50 rounded-lg p-2">
                                <span className="text-blue-600">Outgoing</span>
                                <div className="text-xl font-bold text-blue-700">{relationships?.outgoing.length || 0}</div>
                            </div>
                            <div className="bg-purple-50 rounded-lg p-2">
                                <span className="text-purple-600">Incoming</span>
                                <div className="text-xl font-bold text-purple-700">{relationships?.incoming.length || 0}</div>
                            </div>
                            <div className="bg-green-50 rounded-lg p-2">
                                <span className="text-green-600">Connected Entities</span>
                                <div className="text-xl font-bold text-green-700">{new Set([...relationships!.outgoing.map(r => r.to_entity), ...relationships!.incoming.map(r => r.from_entity)]).size}</div>
                            </div>
                        </div>
                    </Panel>

                    {/* Enhanced Instructions Panel */}
                    <Panel position="bottom-right" className="bg-gradient-to-br from-gray-900 to-gray-800 text-white rounded-xl shadow-2xl p-3 border-2 border-gray-700">
                        <div className="space-y-2 text-xs">
                            <div className="font-bold text-sm mb-2 flex items-center gap-1">
                                <span>💡</span> Interactive Controls
                            </div>
                            <div className="flex items-center gap-2">
                                <span className="bg-white/20 rounded px-1.5 py-0.5 font-mono">Click</span>
                                <span className="text-gray-300">node to view entity</span>
                            </div>
                            <div className="flex items-center gap-2">
                                <span className="bg-white/20 rounded px-1.5 py-0.5 font-mono">Scroll</span>
                                <span className="text-gray-300">to zoom in/out</span>
                            </div>
                            <div className="flex items-center gap-2">
                                <span className="bg-white/20 rounded px-1.5 py-0.5 font-mono">Drag</span>
                                <span className="text-gray-300">canvas to pan</span>
                            </div>
                            <div className="flex items-center gap-2">
                                <span className="bg-white/20 rounded px-1.5 py-0.5 font-mono">Hover</span>
                                <span className="text-gray-300">for details</span>
                            </div>
                        </div>
                    </Panel>
                </ReactFlow>
            </div>
        </div>
    );
};

export default EnhancedRelationshipGraph;

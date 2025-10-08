import React, { useCallback, useEffect } from 'react';
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
} from 'reactflow';
import 'reactflow/dist/style.css';
import { entitiesService } from '../services/entitiesService';
import type { Entity, EntityRelationship } from '../types';
import { useNavigate } from 'react-router-dom';

interface RelationshipGraphProps {
    entity: Entity;
}

// Custom node component for entities
const EntityNode = ({ data }: { data: Record<string, unknown> }) => {
    const navigate = useNavigate();

    const handleClick = () => {
        if (data.entityId && !data.isCurrent) {
            navigate(`/entities/${String(data.entityId)}`);
        }
    };

    return (
        <div
            onClick={handleClick}
            className={`px-4 py-3 rounded-lg border-2 shadow-lg transition-all ${data.isCurrent
                ? 'bg-blue-500 text-white border-blue-600 shadow-blue-200'
                : 'bg-white text-gray-900 border-gray-300 hover:border-blue-400 hover:shadow-xl cursor-pointer'
                }`}
            style={{ minWidth: '150px' }}
        >
            <div className="flex items-center gap-2">
                <div className="text-xl">{String(data.icon || '🔷')}</div>
                <div className="flex-1">
                    <div className="font-semibold text-sm">{String(data.label)}</div>
                    {typeof data.entityType === 'string' && (
                        <div className={`text-xs ${data.isCurrent ? 'text-blue-100' : 'text-gray-500'}`}>
                            {data.entityType}
                        </div>
                    )}
                </div>
            </div>
            {typeof data.relationshipCount === 'number' && (
                <div className={`text-xs mt-1 ${data.isCurrent ? 'text-blue-100' : 'text-gray-500'}`}>
                    {data.relationshipCount} connection{data.relationshipCount !== 1 ? 's' : ''}
                </div>
            )}
        </div>
    );
};

const nodeTypes: NodeTypes = {
    entity: EntityNode,
};

// Layout algorithm - circular layout around center node
const calculateLayout = (
    centerEntity: Entity,
    outgoing: EntityRelationship[],
    incoming: EntityRelationship[]
): { nodes: Node[]; edges: Edge[] } => {
    const nodes: Node[] = [];
    const edges: Edge[] = [];
    const entityMap = new Map<number, { name: string; type: string }>();

    // Add center node
    nodes.push({
        id: `entity-${centerEntity.id}`,
        type: 'entity',
        position: { x: 400, y: 300 },
        data: {
            label: centerEntity.name,
            entityType: centerEntity.entity_type_name,
            entityId: centerEntity.id,
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

    // Calculate positions in a circle around the center
    const relatedEntities = Array.from(entityMap.entries());
    const radius = 300;
    const angleStep = (2 * Math.PI) / relatedEntities.length;

    relatedEntities.forEach(([entityId, info], index) => {
        const angle = index * angleStep;
        const x = 400 + radius * Math.cos(angle);
        const y = 300 + radius * Math.sin(angle);

        nodes.push({
            id: `entity-${entityId}`,
            type: 'entity',
            position: { x, y },
            data: {
                label: info.name,
                entityType: info.type,
                entityId: entityId,
                isCurrent: false,
            },
        });
    });

    // Add edges for outgoing relationships
    outgoing.forEach((rel) => {
        const strengthColor =
            rel.strength >= 8 ? '#ef4444' : // red for strong
                rel.strength >= 5 ? '#f59e0b' : // amber for medium
                    '#10b981'; // green for weak

        edges.push({
            id: `edge-out-${rel.id}`,
            source: `entity-${centerEntity.id}`,
            target: `entity-${rel.to_entity}`,
            type: 'smoothstep',
            animated: rel.strength >= 8,
            style: {
                stroke: strengthColor,
                strokeWidth: Math.max(1, rel.strength / 2),
            },
            markerEnd: {
                type: MarkerType.ArrowClosed,
                color: strengthColor,
            },
            label: rel.relationship_type,
            labelStyle: {
                fill: '#64748b',
                fontSize: 11,
                fontWeight: 500,
            },
            labelBgStyle: {
                fill: '#ffffff',
                fillOpacity: 0.9,
            },
        });
    });

    // Add edges for incoming relationships
    incoming.forEach((rel) => {
        const strengthColor =
            rel.strength >= 8 ? '#ef4444' :
                rel.strength >= 5 ? '#f59e0b' :
                    '#10b981';

        edges.push({
            id: `edge-in-${rel.id}`,
            source: `entity-${rel.from_entity}`,
            target: `entity-${centerEntity.id}`,
            type: 'smoothstep',
            animated: rel.strength >= 8,
            style: {
                stroke: strengthColor,
                strokeWidth: Math.max(1, rel.strength / 2),
            },
            markerEnd: {
                type: MarkerType.ArrowClosed,
                color: strengthColor,
            },
            label: rel.relationship_type,
            labelStyle: {
                fill: '#64748b',
                fontSize: 11,
                fontWeight: 500,
            },
            labelBgStyle: {
                fill: '#ffffff',
                fillOpacity: 0.9,
            },
        });
    });

    return { nodes, edges };
};

const RelationshipGraph: React.FC<RelationshipGraphProps> = ({ entity }) => {
    const [nodes, setNodes, onNodesChange] = useNodesState([]);
    const [edges, setEdges, onEdgesChange] = useEdgesState([]);

    // Fetch relationships
    const { data: relationships, isLoading, error } = useQuery({
        queryKey: ['entity-relationships', entity.id],
        queryFn: () => entitiesService.getEntityRelationships(entity.id),
    });

    // Update graph when relationships change
    useEffect(() => {
        if (relationships) {
            const { nodes: newNodes, edges: newEdges } = calculateLayout(
                entity,
                relationships.outgoing,
                relationships.incoming
            );
            setNodes(newNodes);
            setEdges(newEdges);
        }
    }, [relationships, entity, setNodes, setEdges]);

    const onNodeClick = useCallback((_: React.MouseEvent, node: Node) => {
        // Node selection could be used for future features
        console.log('Selected node:', node.id);
    }, []);

    if (isLoading) {
        return (
            <div className="flex items-center justify-center h-96">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
                    <p className="text-gray-600">Loading relationship graph...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="text-center py-12">
                <div className="text-red-400 text-5xl mb-4">⚠️</div>
                <h3 className="text-lg font-medium text-gray-900 mb-2">
                    Error Loading Graph
                </h3>
                <p className="text-gray-600">
                    Failed to load relationship data. Please try again.
                </p>
            </div>
        );
    }

    const totalRelationships = (relationships?.outgoing.length || 0) + (relationships?.incoming.length || 0);

    if (totalRelationships === 0) {
        return (
            <div className="text-center py-12">
                <div className="text-gray-400 text-5xl mb-4">🔗</div>
                <h3 className="text-lg font-medium text-gray-900 mb-2">
                    No Relationships Found
                </h3>
                <p className="text-gray-600 mb-4">
                    This entity doesn't have any relationships yet.
                </p>
                <p className="text-sm text-gray-500">
                    Add relationships in the "Relationships" tab to see them visualized here.
                </p>
            </div>
        );
    }

    return (
        <div className="h-[600px] bg-gray-50 rounded-lg border border-gray-200 relative">
            <ReactFlow
                nodes={nodes}
                edges={edges}
                onNodesChange={onNodesChange}
                onEdgesChange={onEdgesChange}
                onNodeClick={onNodeClick}
                nodeTypes={nodeTypes}
                connectionLineType={ConnectionLineType.SmoothStep}
                fitView
                attributionPosition="bottom-left"
                className="bg-gray-50"
            >
                <Background color="#e5e7eb" gap={16} />
                <Controls />
                <MiniMap
                    nodeColor={(node) => {
                        if (node.data.isCurrent) return '#3b82f6';
                        return '#94a3b8';
                    }}
                    maskColor="rgba(0, 0, 0, 0.1)"
                />

                {/* Info Panel */}
                <Panel position="top-left" className="bg-white rounded-lg shadow-lg p-4 border border-gray-200">
                    <h3 className="font-semibold text-gray-900 mb-2">
                        Relationship Graph
                    </h3>
                    <div className="space-y-1 text-sm text-gray-600">
                        <div className="flex items-center gap-2">
                            <div className="w-3 h-3 bg-blue-500 rounded"></div>
                            <span>Current Entity</span>
                        </div>
                        <div className="flex items-center gap-2">
                            <div className="w-3 h-3 bg-white border-2 border-gray-300 rounded"></div>
                            <span>Related Entities</span>
                        </div>
                        <div className="pt-2 border-t border-gray-200 mt-2">
                            <div className="flex items-center gap-2 mb-1">
                                <div className="w-8 h-0.5 bg-green-500"></div>
                                <span className="text-xs">Weak (1-4)</span>
                            </div>
                            <div className="flex items-center gap-2 mb-1">
                                <div className="w-8 h-0.5 bg-amber-500"></div>
                                <span className="text-xs">Medium (5-7)</span>
                            </div>
                            <div className="flex items-center gap-2">
                                <div className="w-8 h-0.5 bg-red-500"></div>
                                <span className="text-xs">Strong (8-10)</span>
                            </div>
                        </div>
                    </div>
                </Panel>

                {/* Stats Panel */}
                <Panel position="top-right" className="bg-white rounded-lg shadow-lg p-4 border border-gray-200">
                    <div className="space-y-2 text-sm">
                        <div>
                            <span className="text-gray-600">Total Connections:</span>
                            <span className="ml-2 font-semibold text-gray-900">{totalRelationships}</span>
                        </div>
                        <div>
                            <span className="text-gray-600">Outgoing:</span>
                            <span className="ml-2 font-semibold text-blue-600">{relationships?.outgoing.length || 0}</span>
                        </div>
                        <div>
                            <span className="text-gray-600">Incoming:</span>
                            <span className="ml-2 font-semibold text-purple-600">{relationships?.incoming.length || 0}</span>
                        </div>
                    </div>
                </Panel>

                {/* Instructions Panel */}
                <Panel position="bottom-right" className="bg-white/90 backdrop-blur rounded-lg shadow-lg p-3 border border-gray-200">
                    <div className="space-y-1 text-xs text-gray-600">
                        <div>🖱️ <strong>Click</strong> node to view entity</div>
                        <div>🔍 <strong>Scroll</strong> to zoom</div>
                        <div>✋ <strong>Drag</strong> to pan</div>
                    </div>
                </Panel>
            </ReactFlow>
        </div>
    );
};

export default RelationshipGraph;

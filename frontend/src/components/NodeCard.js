import React from 'react';
import { useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';

export default function NodeCard({ node }) {
    const { attributes, listeners, setNodeRef, transform, transition } = useSortable({ id: node.id });

    const style = {
        transform: CSS.Transform.toString(transform),
        transition,
        border: '1px solid #ccc',
        padding: 10,
        marginBottom: 8,
        background: '#fff',
    };

    return (
        <div ref={setNodeRef} style={style} {...attributes} {...listeners}>
            <strong>{node.type}</strong>
            <pre style={{ fontSize: 11 }}>
                {JSON.stringify(node.params, null, 2)}
            </pre>
        </div>
    );
}
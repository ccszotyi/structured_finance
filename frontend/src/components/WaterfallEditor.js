import React from "react";
import { DndContext } from "@dnd-kit/core";
import { SortableContext, arrayMove } from "@dnd-kit/sortable";
import NodeCard from "./NodeCard";
import { patchDeal, runDeal } from "../api";

export default function WaterfallEditor({ deal, setDeal }) {
    const nodes = deal.waterfall || [];

    function onDragEnd(e) {
        const { active, over } = e;
        if (!over || active.id === over.id) return;

        const oldI = nodes.findIndex((n) => n.id === active.id);
        const newI = nodes.findIndex((n) => n.id === over.id);
        const reordered = arrayMove(nodes, oldI, newI);

        const updated = { ...deal, waterfall: reordered };
        setDeal(updated);
        patchDeal(deal.id, { waterfall: reordered });
    }

    async function run() {
        const res = await runDeal(deal.id);
        console.log("Deal run result:", res);
    }

    return (
        <div style={{ display: "flex", gap: 20 }}>
            <DndContext onDragEnd={onDragEnd}>
                <SortableContext items={nodes.map((n) => n.id)}>
                    <div style={{ width: 320 }}>
                        {nodes.map(n => (
                            <NodeCard key={n.id} node={n} />
                        ))}
                    </div>
                </SortableContext>
            </DndContext>

            <div>
                <button onClick={run}>Run Deal</button>
            </div>
        </div>
    );
}
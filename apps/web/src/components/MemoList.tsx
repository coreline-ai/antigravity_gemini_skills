"use client";

import { useEffect, useState } from "react";
import { useMemoStore } from "@/store/memo";

export default function MemoList() {
    const { memos, loadMemos, deleteMemo, updateMemo } = useMemoStore();
    const [editingId, setEditingId] = useState<string | null>(null);
    const [editContent, setEditContent] = useState("");

    useEffect(() => {
        loadMemos();
    }, [loadMemos]);

    const startEditing = (id: string, content: string) => {
        setEditingId(id);
        setEditContent(content);
    };

    const saveEdit = (id: string) => {
        if (editContent.trim()) {
            updateMemo(id, editContent);
        }
        setEditingId(null);
    };

    if (memos.length === 0) {
        return (
            <div className="text-center text-gray-500 py-10">
                No memos yet. Write something above!
            </div>
        );
    }

    return (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {memos.map((memo) => (
                <div
                    key={memo.id}
                    className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow border border-gray-200 dark:border-gray-700 flex flex-col justify-between group"
                >
                    {editingId === memo.id ? (
                        <div className="flex flex-col gap-2">
                            <textarea
                                value={editContent}
                                onChange={(e) => setEditContent(e.target.value)}
                                className="w-full p-2 border rounded dark:bg-gray-900 dark:border-gray-600 dark:text-white"
                                rows={3}
                                autoFocus
                            />
                            <div className="flex justify-end gap-2">
                                <button
                                    onClick={() => setEditingId(null)}
                                    className="px-3 py-1 text-sm text-gray-600 hover:bg-gray-100 rounded dark:text-gray-300 dark:hover:bg-gray-700"
                                >
                                    Cancel
                                </button>
                                <button
                                    onClick={() => saveEdit(memo.id)}
                                    className="px-3 py-1 text-sm bg-blue-600 text-white rounded hover:bg-blue-700"
                                >
                                    Save
                                </button>
                            </div>
                        </div>
                    ) : (
                        <>
                            <p className="whitespace-pre-wrap dark:text-gray-200 mb-4 break-words">
                                {memo.content}
                            </p>
                            <div className="flex justify-between items-center text-sm text-gray-500 border-t pt-3 dark:border-gray-700">
                                <span>{new Date(memo.createdAt).toLocaleDateString()}</span>
                                <div className="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                                    <button
                                        onClick={() => startEditing(memo.id, memo.content)}
                                        className="text-blue-500 hover:text-blue-700"
                                    >
                                        Edit
                                    </button>
                                    <button
                                        onClick={() => deleteMemo(memo.id)}
                                        className="text-red-500 hover:text-red-700"
                                    >
                                        Delete
                                    </button>
                                </div>
                            </div>
                        </>
                    )}
                </div>
            ))}
        </div>
    );
}

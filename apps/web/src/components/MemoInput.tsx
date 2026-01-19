"use client";

import { useState } from "react";
import { useMemoStore } from "@/store/memo";

export default function MemoInput() {
    const [content, setContent] = useState("");
    const addMemo = useMemoStore((state) => state.addMemo);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (!content.trim()) return;
        addMemo(content);
        setContent("");
    };

    return (
        <form onSubmit={handleSubmit} className="mb-8">
            <div className="flex gap-2">
                <input
                    type="text"
                    value={content}
                    onChange={(e) => setContent(e.target.value)}
                    placeholder="What's on your mind?"
                    className="flex-1 p-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:border-gray-700 dark:text-white"
                />
                <button
                    type="submit"
                    disabled={!content.trim()}
                    className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                    Add
                </button>
            </div>
        </form>
    );
}

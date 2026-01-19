import { Memo } from "@/types/memo";

const STORAGE_KEY = "simple-memo-app-data";

export const MemoService = {
    getAll: (): Memo[] => {
        if (typeof window === "undefined") return [];
        const data = localStorage.getItem(STORAGE_KEY);
        return data ? JSON.parse(data) : [];
    },

    saveAll: (memos: Memo[]) => {
        if (typeof window === "undefined") return;
        localStorage.setItem(STORAGE_KEY, JSON.stringify(memos));
    },

    create: (content: string): Memo => {
        const newMemo: Memo = {
            id: crypto.randomUUID(),
            content,
            createdAt: Date.now(),
            updatedAt: Date.now(),
        };
        const memos = MemoService.getAll();
        memos.unshift(newMemo);
        MemoService.saveAll(memos);
        return newMemo;
    },

    update: (id: string, content: string): Memo | null => {
        const memos = MemoService.getAll();
        const index = memos.findIndex((m) => m.id === id);
        if (index === -1) return null;

        memos[index] = {
            ...memos[index],
            content,
            updatedAt: Date.now(),
        };
        MemoService.saveAll(memos);
        return memos[index];
    },

    delete: (id: string): void => {
        const memos = MemoService.getAll();
        const filtered = memos.filter((m) => m.id !== id);
        MemoService.saveAll(filtered);
    },
};

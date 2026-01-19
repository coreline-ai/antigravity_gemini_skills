import { create } from "zustand";
import { Memo } from "@/types/memo";
import { MemoService } from "@/services/memo";

interface MemoState {
    memos: Memo[];
    loadMemos: () => void;
    addMemo: (content: string) => void;
    updateMemo: (id: string, content: string) => void;
    deleteMemo: (id: string) => void;
}

export const useMemoStore = create<MemoState>((set) => ({
    memos: [],

    loadMemos: () => {
        const memos = MemoService.getAll();
        set({ memos });
    },

    addMemo: (content) => {
        const newMemo = MemoService.create(content);
        set((state) => ({ memos: [newMemo, ...state.memos] }));
    },

    updateMemo: (id, content) => {
        const updated = MemoService.update(id, content);
        if (updated) {
            set((state) => ({
                memos: state.memos.map((m) => (m.id === id ? updated : m)),
            }));
        }
    },

    deleteMemo: (id) => {
        MemoService.delete(id);
        set((state) => ({
            memos: state.memos.filter((m) => m.id !== id),
        }));
    },
}));

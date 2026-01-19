"use client";

import MemoInput from "@/components/MemoInput";
import MemoList from "@/components/MemoList";

export default function Home() {
  return (
    <main className="min-h-screen p-8 bg-gray-50 dark:bg-gray-900">
      <div className="max-w-4xl mx-auto">
        <header className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            Simple Memo
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Your ideas, safely stored in your browser.
          </p>
        </header>

        <MemoInput />
        <MemoList />
      </div>
    </main>
  );
}

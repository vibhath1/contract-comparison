import { EvervaultCard } from "../components/EvervaultCard";

export function EvervaultCardDemo() {
  return (
    <div>
      <div className="flex flex-col gap-5 w-full">
      <div className="flex justify-start items-start gap-5 w-full">
        {/* Left column */}
        <div className="flex flex-col gap-5 max-w-sm w-full">
        {/* Top left box */}
        <div className="glass-effectstyle hover:bg-transparent transition-colors duration-500 ease-in-out border rounded-xl border-white/[0.2] dark:border-white/[0.2] flex flex-col items-start p-4 relative h-[30rem] shadow-sm">
          <EvervaultCard text="Introducing our Contract Comparison AI" />
        </div>
        {/* Bottom left box, same height as lower right box */}
        <div className=" glass-effectstyle hover:bg-transparent transition-colors duration-500 ease-in-out border rounded-xl border-white/[0.2] dark:border-white/[0.2] flex flex-col items-start p-4 relative h-[15rem] shadow-sm">
        
        </div>
        </div>
        {/* Right column */}
        <div className="flex flex-col justify-center items-center gap-5 w-full">
        {/* Right top box */}
        <div
          className="glass-effectstyle hover:bg-transparent transition-colors duration-500 ease-in-out border rounded-xl border-white/[0.2] dark:border-white/[0.2] flex items-center justify-center p-10 relative h-[15rem] w-auto max-w-full">
          <p className="max-w-[500px] text-[#dbdbdb] text-[20px] leading-[30px]">
          Our Tool allows you to compare two documents. Make your contract comparisons quick and easy. Upload PDFs and Word format documents, hit compare and share with a private URL.
          </p>
        </div>
        {/* Lower Right box */}
        <div
          className="glass-effectstyle hover:bg-transparent transition-colors duration-500 ease-in-out border rounded-xl border-white/[0.2] dark:border-white/[0.2] flex items-center justify-center p-10 relative h-[30rem] w-auto max-w-full">
          <p className="max-w-[500px] text-[#dbdbdb] text-[20px] leading-[30px]">
          Our Tool allows you to compare two documents. Make your contract comparisons quick and easy. Upload PDFs and Word format documents, hit compare and share with a private URL.
          </p>
        </div>
        </div>
      </div>
      </div>
    </div>
  );
}

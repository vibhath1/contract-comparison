import React from "react";
import { EvervaultCard, Icon } from "../components/EvervaultCard";

export function EvervaultCardDemo() {
  return (
   <>
    <div className="flex justify-start items-start gap-8 w-full">
      {/* Left box: fixed max width, aligned left */}
      <div className="glass-effectstyle hover:bg-transparent border rounded-xl border-white/[0.2] dark:border-white/[0.2] flex flex-col items-start max-w-sm p-4 relative h-[30rem] shadow-sm" >
        <EvervaultCard text="Introducing our Contract Comparison AI" />
      </div>



      {/* Right box: width auto based on content */}
      <div className="border rounded-xl border-white/[0.2] dark:border-white/[0.2] flex items-center justify-center p-10 relative h-[15rem] w-auto max-w-full"
      style={{ background: "rgba(255,255,255,0.04)",
                  backdropFilter: "blur(10px)",
                  boxShadow: "0 4px 30px rgba(0, 0, 0, 0.1)",
                  WebkitBackdropFilter: "blur(10px)",
       }}>
        <p className="max-w-[650px] text-[#dbdbdb] text-[20px] leading-[30px]"> 

          Our Tool allows you to compare two documents. Make your contract comparisons quick and easy. Upload PDFs and Word format documents, hit compare and share with a private URL.
        </p>
      </div>
    </div>

    
    </>
  );
}

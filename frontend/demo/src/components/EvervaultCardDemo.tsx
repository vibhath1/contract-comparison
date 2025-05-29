import React from "react";
import { EvervaultCard, Icon } from "../components/EvervaultCard";

export function EvervaultCardDemo() {
  return (
   <>
    <div className="border rounded-xl border-white/[0.2] dark:border-white/[0.2] flex flex-col items-start max-w-sm mx-auto p-4 relative h-[30rem]">
      {/*<div className="font-bold text-[50px] absolute top-[50%] left-1/2 transform -translate-x-1/2 -translate-y-1/2 h-6 w-16 dark:text-white text-white z-10 flex items-center justify-center">
  Introducing our Contract Comparison AI
</div>*/}

      <EvervaultCard text="Introducing our Contract Comparison AI"/>
      {/*<h2 className="dark:text-white text-white mt-4 text-sm font-light">
        Hover over this card to reveal an awesome effect.
      </h2>*/}
    </div>


    <div className="border rounded-xl border-white/[0.2] dark:border-white/[0.2] flex flex-col items-start mx-auto p-4 relative h-[30rem] ">
      {/*<div className="font-bold text-[50px] absolute top-[50%] left-1/2 transform -translate-x-1/2 -translate-y-1/2 h-6 w-16 dark:text-white text-white z-10 flex items-center justify-center">
  Introducing our Contract Comparison AI
</div>*/}

      <EvervaultCard text="Our Tool allows you to compare two documentsMake you contract comparisons quick and easy. Upload PDFs and Word format documents, hit compare and share with a private URL. Simple and quick."/>
      {/*<h2 className="dark:text-white text-white mt-4 text-sm font-light">
        Hover over this card to reveal an awesome effect.
      </h2>*/}
    </div>

    
    </>
  );
}

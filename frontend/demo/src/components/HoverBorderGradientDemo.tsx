"use client";
import { HoverBorderGradient } from "../components/HoverBorderGradient";

export function HoverBorderGradientDemo() {
  return (
    <div className="m-5 flex justify-center text-center">
      <HoverBorderGradient
        containerClassName="rounded-full"
        as="button"
        className=" bg-transparent text-white dark:text-white flex items-center space-x-2"
      >
        <div>
        <span>Compare.</span>
        </div>
      </HoverBorderGradient>
    </div>
  );
}
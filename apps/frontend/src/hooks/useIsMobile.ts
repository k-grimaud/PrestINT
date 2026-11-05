// hooks/useIsMobile.ts
"use client"

import { useState, useEffect } from 'react';

const useIsMobile = (maxWidth: number = 768): boolean => {
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth < maxWidth);
    };

    // Set the initial value
    handleResize();

    window.addEventListener('resize', handleResize);

    // Cleanup the event listener
    return () => window.removeEventListener('resize', handleResize);
  }, [maxWidth]);

  return isMobile;
};

export default useIsMobile;
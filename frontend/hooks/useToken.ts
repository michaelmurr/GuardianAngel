import { useAuth } from "@clerk/clerk-expo";
import { useCallback } from "react";




export function useToken() {
  const { getToken } = useAuth()

  return useCallback(async () => {
    return getToken({ template: "test" })
  }, [getToken])
}
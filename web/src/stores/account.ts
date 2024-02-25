import { hookstate, useHookstate } from "@hookstate/core";

interface AccountState {
  address: string | null;
}

const initialState = hookstate<AccountState>({
  address: null,
});

export const useAccountState = () => {
  const state = useHookstate(initialState);

  return {
    getAddress: () => state.address.get(),
    setAddress: (address: string) => state.address.set(address),
  };
};
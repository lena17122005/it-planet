import { createContext, useMemo, useReducer, type PropsWithChildren } from 'react';
import type { AuthUser } from '../types';

interface AuthState {
  user: AuthUser | null;
}

type AuthAction =
  | { type: 'LOGIN'; payload: AuthUser }
  | { type: 'LOGOUT' };

const storedUser = localStorage.getItem('tramplin_user');
const initialState: AuthState = { user: storedUser ? JSON.parse(storedUser) : null };

function reducer(state: AuthState, action: AuthAction): AuthState {
  switch (action.type) {
    case 'LOGIN':
      return { ...state, user: action.payload };
    case 'LOGOUT':
      return { ...state, user: null };
    default:
      return state;
  }
}

export const AuthContext = createContext<{
  state: AuthState;
  login: (user: AuthUser) => void;
  logout: () => void;
}>({
  state: initialState,
  login: () => undefined,
  logout: () => undefined
});

export function AuthProvider({ children }: PropsWithChildren) {
  const [state, dispatch] = useReducer(reducer, initialState);

  const value = useMemo(
    () => ({
      state,
      login: (user: AuthUser) => {
        localStorage.setItem('tramplin_user', JSON.stringify(user));
        dispatch({ type: 'LOGIN', payload: user });
      },
      logout: () => {
        localStorage.removeItem('tramplin_user');
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        dispatch({ type: 'LOGOUT' });
      }
    }),
    [state]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

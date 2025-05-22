import { ClerkProvider } from '@clerk/clerk-expo'
import { tokenCache } from '@clerk/clerk-expo/token-cache'
import { ToastProvider, ToastViewport } from '@tamagui/toast'
import { EXPO_PUBLIC_CLERK_PUBLISHABLE_KEY } from 'constants/Key'
import { useColorScheme } from 'react-native'
import { TamaguiProvider, type TamaguiProviderProps } from 'tamagui'
import { config } from '../tamagui.config'
import { CurrentToast } from './CurrentToast'

export function Provider({ children, ...rest }: Omit<TamaguiProviderProps, 'config'>) {
  const colorScheme = useColorScheme()

  return (
    <TamaguiProvider
      config={config}
      defaultTheme={'light'}
      {...rest}
    >
      <ClerkProvider tokenCache={tokenCache} publishableKey={EXPO_PUBLIC_CLERK_PUBLISHABLE_KEY}>
        <ToastProvider
          swipeDirection="horizontal"
          duration={6000}
          native={
            [
              // uncomment the next line to do native toasts on mobile. NOTE: it'll require you making a dev build and won't work with Expo Go
              // 'mobile'
            ]
          }
        >
          {children}
          <CurrentToast />
          <ToastViewport top="$8" left={0} right={0} />

        </ToastProvider>
      </ClerkProvider>
    </TamaguiProvider>
  )
}

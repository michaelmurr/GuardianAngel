import { useAuth, useClerk, useSignIn } from '@clerk/clerk-expo'
import { HeadingH2 } from 'components/Headings'
import { PrimaryBtn } from 'components/PrimaryBtn'
import { Link, useRouter } from 'expo-router'
import { useToken } from 'hooks/useToken'
import React, { useEffect } from 'react'
import { SafeAreaView, Text, TextInput, TouchableOpacity, View } from 'react-native'
import { Button, Input, YStack } from 'tamagui'

export default function Page() {
        const { signIn, setActive, isLoaded } = useSignIn()
        const { signOut } = useClerk()
        const router = useRouter()

        const [emailAddress, setEmailAddress] = React.useState('michael.murr04@gmail.com')
        const [password, setPassword] = React.useState(';alsdfasdlfjewrhqui3rn')
        const getToken = useToken()

        // Handle the submission of the sign-in form
        const onSignInPress = async () => {
                if (!isLoaded) return
                console.log('pressed')
                // Start the sign-in process using the email and password provided
                try {
                        const signInAttempt = await signIn.create({
                                identifier: emailAddress,
                                password,
                        })

                        // If sign-in process is complete, set the created session as active
                        // and redirect the user
                        if (signInAttempt.status === 'complete') {
                                await setActive({ session: signInAttempt.createdSessionId })

                                const token = await getToken();
                                console.log(
                                        '%capp/(auth)/sign-in.tsx:32 token',
                                        'color: #007acc;',
                                        JSON.stringify(token, null, "\t")
                                );
                                router.replace('/')
                        } else {
                                // If the status isn't complete, check why. User might need to
                                // complete further steps.
                                console.error(JSON.stringify(signInAttempt, null, 2))
                        }
                } catch (err) {
                        // See https://clerk.com/docs/custom-flows/error-handling
                        // for more info on error handling
                        console.error(JSON.stringify(err, null, 2))
                }
        }

        return (
                <YStack gap={"$2"} p="$2" bg={"$background"} pt="$12" flex={1} >
                        {/* <HeadingH2>Sign in</HeadingH2> */}
                        <Input
                                autoCapitalize="none"
                                value={emailAddress}
                                placeholder="Enter email"
                                onChangeText={(emailAddress) => setEmailAddress(emailAddress)}
                        />
                        <Input
                                value={password}
                                placeholder="Enter password"
                                secureTextEntry={true}
                                onChangeText={(password) => setPassword(password)}
                        />
                        <View style={{ display: 'flex', flexDirection: 'row', gap: 3 }}>
                                <Text>Don't have an account?</Text>
                                <Link href="/sign-up">
                                        <Text>Sign up</Text>
                                </Link>
                        </View>
                        <PrimaryBtn onPress={() => onSignInPress()}>Sign in
                        </PrimaryBtn>
                        <PrimaryBtn onPress={async () => await signOut()}>Sign out</PrimaryBtn>
                </YStack>
        )
}
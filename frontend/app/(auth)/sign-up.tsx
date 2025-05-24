import { useAuth, useSignUp } from '@clerk/clerk-expo'
import { HeadingH2 } from 'components/Headings'
import { PrimaryBtn } from 'components/PrimaryBtn'
import { API_URL } from 'constants/Key'
import { Link, useRouter } from 'expo-router'
import { useToken } from 'hooks/useToken'
import * as React from 'react'
import { Text, TextInput, TouchableOpacity, View } from 'react-native'
import { Input, YStack } from 'tamagui'

export default function SignUpScreen() {
        const { isLoaded, signUp, setActive } = useSignUp()
        const router = useRouter()
        const getToken = useToken()
        const [emailAddress, setEmailAddress] = React.useState('michael.murr04@gmail.com')
        const [password, setPassword] = React.useState(';alsdfasdlfjewrhqui3rn')
        const [pendingVerification, setPendingVerification] = React.useState(false)
        const [code, setCode] = React.useState('')
        const [firstname, setFirstname] = React.useState('');
        const [lastname, setLastname] = React.useState('')

        // Handle submission of sign-up form
        const onSignUpPress = async () => {
                console.log('first')
                if (!isLoaded) return


                console.log(emailAddress, password)

                // Start sign-up process using email and password provided
                try {
                        await signUp.create({
                                firstName: firstname,
                                lastName: lastname,
                                emailAddress,
                                password,
                        })

                        // Send user an email with verification code
                        await signUp.prepareEmailAddressVerification({ strategy: 'email_code' })

                        // Set 'pendingVerification' to true to display second form
                        // and capture OTP code
                        setPendingVerification(true)
                } catch (err) {
                        // See https://clerk.com/docs/custom-flows/error-handling
                        // for more info on error handling
                        console.error(JSON.stringify(err, null, 2))
                }
        }

        // Handle submission of verification form
        const onVerifyPress = async () => {
                if (!isLoaded) return

                try {
                        // Use the code the user provided to attempt verification
                        const signUpAttempt = await signUp.attemptEmailAddressVerification({
                                code,
                        })

                        // If verification was completed, set the session to active
                        // and redirect the user
                        if (signUpAttempt.status === 'complete') {
                                await setActive({ session: signUpAttempt.createdSessionId })
                                const token = await getToken();
                                console.log(
                                        '%capp/(auth)/sign-up.tsx:65 token',
                                        'color: #007acc;',
                                        JSON.stringify(token, null, "\t")
                                );


                                const res = await fetch(`${API_URL}/users/me`, {
                                        headers: {
                                                Authorization: `Bearer ${token}`
                                        }
                                })
                                const json = await res.json();

                                console.log(
                                        '%capp/(auth)/sign-up.tsx:71 json',
                                        'color: #007acc;',
                                        JSON.stringify(json, null, "\t")
                                );
                                router.replace('/')
                        } else {
                                // If the status is not complete, check why. User may need to
                                // complete further steps.
                                console.error(JSON.stringify(signUpAttempt, null, 2))
                        }
                } catch (err) {
                        // See https://clerk.com/docs/custom-flows/error-handling
                        // for more info on error handling
                        console.error(JSON.stringify(err, null, 2))
                }
        }

        if (pendingVerification) {
                return (
                        <>
                                <Text>Verify your email</Text>
                                <TextInput
                                        value={code}
                                        placeholder="Enter your verification code"
                                        onChangeText={(code) => setCode(code)}
                                />
                                <TouchableOpacity onPress={onVerifyPress}>
                                        <Text>Verify</Text>
                                </TouchableOpacity>
                        </>
                )
        }

        return (
                <YStack gap={"$2"} p="$2" bg={"$background"} pt="$12" flex={1} >

                        <>
                                {/* <HeadingH2>Create Account</HeadingH2> */}
                                <Input
                                        autoCapitalize="none"
                                        value={firstname}
                                        placeholder="First name"
                                        onChangeText={(e) => setFirstname(e)}
                                />
                                <Input
                                        autoCapitalize="none"
                                        value={lastname}
                                        placeholder="Last name"
                                        onChangeText={(e) => setLastname(e)}
                                />

                                <Input
                                        autoCapitalize="none"
                                        value={emailAddress}
                                        placeholder="Enter email"
                                        onChangeText={(email) => setEmailAddress(email)}
                                />
                                <Input
                                        value={password}
                                        placeholder="Enter password"
                                        secureTextEntry={true}
                                        onChangeText={(password) => setPassword(password)}
                                />
                                <View style={{ display: 'flex', flexDirection: 'row', gap: 3 }}>
                                        <Text>Already have an account?</Text>
                                        <Link href="/sign-in">
                                                <Text>Sign in</Text>
                                        </Link>
                                </View>
                                <PrimaryBtn onPress={onSignUpPress}>
                                        Continue
                                </PrimaryBtn>
                        </>
                </YStack>
        )
}
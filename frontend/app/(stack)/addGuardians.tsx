import { HeadingH2 } from 'components/Headings';
import { PrimaryBtn } from 'components/PrimaryBtn';
import { useRouter } from 'expo-router';
import React from 'react';
import { SafeAreaView } from 'react-native';
import { Avatar, Input, Text, XStack, YStack } from 'tamagui';

const AddGuardians = () => {
        const router = useRouter();
        const handleSearchUser = (e) => {
                //fetch the username
        }
        return (
                <SafeAreaView>

                        <YStack p="$2">
                                <HeadingH2>Add your guardian</HeadingH2>
                                <PrimaryBtn onPress={() => router.replace('/')}>Back</PrimaryBtn>
                                <XStack gap={"$2"}>
                                        <Avatar circular size="$5">
                                                <Avatar.Image
                                                        accessibilityLabel="Cam"
                                                        src="https://images.unsplash.com/photo-1548142813-c348350df52b?&w=150&h=150&dpr=2&q=80"
                                                />
                                                <Avatar.Fallback backgroundColor="$blue10" />
                                        </Avatar>
                                        <Avatar circular size="$5">
                                                <Avatar.Image
                                                        accessibilityLabel="Cam"
                                                        src="https://images.unsplash.com/photo-1548142813-c348350df52b?&w=150&h=150&dpr=2&q=80"
                                                />
                                                <Avatar.Fallback backgroundColor="$blue10" />
                                        </Avatar>
                                        <Avatar circular size="$5">
                                                <Avatar.Image
                                                        accessibilityLabel="Cam"
                                                        src="https://images.unsplash.com/photo-1548142813-c348350df52b?&w=150&h=150&dpr=2&q=80"
                                                />
                                                <Avatar.Fallback backgroundColor="$blue10" />
                                        </Avatar>
                                </XStack>
                                <Input size={"$4"} placeholder={`Search Username`} onChange={(e) => handleSearchUser(e)} />
                        </YStack>
                </SafeAreaView>
        )
}

export default AddGuardians;
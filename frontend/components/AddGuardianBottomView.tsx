import { BottomSheetView } from "@gorhom/bottom-sheet";
import { ChevronDown, Plus } from "@tamagui/lucide-icons";
import { StyleSheet, TouchableOpacity } from "react-native";
import { Avatar, Input, Text, XStack, YStack } from "tamagui";
import BottomSheetHeader from "./BottomSheetHeader";
import { PrimaryBtn } from "./PrimaryBtn";

const AddGuardianBottomView = ({ expandSheet, members, users, searchTerm, setSearchTerm, handleAddUser, setShowSelectRoute, }) => (
        <BottomSheetView style={styles.contentContainer}>
                <YStack px="$4" gap={"$4"}>
                        <BottomSheetHeader title={'Add Guardians'} members={members} expandSheet={expandSheet} />

                </YStack>

                <YStack width="95%" px="$2" gap="$2" justify={"space-between"} height={"80%"}>
                        <YStack>

                                <Input
                                        value={searchTerm}
                                        onChangeText={setSearchTerm}
                                        placeholder="Search by username"
                                        width="100%"
                                        alignSelf="center"
                                        marginVertical="$4"
                                />

                                <YStack gap="$2" flexWrap="wrap">
                                        {users.map((user, idx) => (
                                                <XStack
                                                        key={idx}
                                                        justify="space-between"
                                                        alignItems="center"
                                                        bg="$white2"
                                                        py="$2"
                                                        pr="$4"
                                                        pl="$2"
                                                        rounded="$4"
                                                        borderColor="$white5"
                                                        borderWidth="1"
                                                >
                                                        <XStack flex={1} gap="$4" alignItems="center" width={80}>
                                                                <Avatar circular size="$4">
                                                                        <Avatar.Image accessibilityLabel={user.name} src={members[idx].avatar} />
                                                                </Avatar>
                                                                <Text fontWeight="500" fontSize="$5" width={"100%"}>{user.name}</Text>
                                                        </XStack>
                                                        <TouchableOpacity onPress={() => handleAddUser(user.username)}>

                                                                <XStack alignItems="center" >
                                                                        <Plus color="$white11" />
                                                                        <Text fontWeight="500" color="$white11">Add</Text>
                                                                </XStack>
                                                        </TouchableOpacity>
                                                </XStack>
                                        ))}
                                </YStack>
                        </YStack>

                        <PrimaryBtn onPress={() => setShowSelectRoute(true)} icon={ChevronDown} theme="gray" marginTop="$4">
                                Next
                        </PrimaryBtn>
                </YStack>

        </BottomSheetView>
)

export default AddGuardianBottomView;

const styles = StyleSheet.create({
        contentContainer: {
                flex: 1,
                alignItems: 'center',
        },
})
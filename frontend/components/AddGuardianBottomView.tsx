import { BottomSheetView } from "@gorhom/bottom-sheet";
import {
  ChevronDown,
  ChevronRight,
  CirclePlus,
  Plus,
  UserRoundPlus,
} from "@tamagui/lucide-icons";
import { StyleSheet, TouchableOpacity } from "react-native";
import { Avatar, Button, Input, Text, XStack, YStack } from "tamagui";
import BottomSheetHeader from "./BottomSheetHeader";
import { PrimaryBtn } from "./PrimaryBtn";
import { Pressable } from "react-native-gesture-handler";

const AddGuardianBottomView = ({
  expandSheet,
  members,
  users,
  searchTerm,
  setSearchTerm,
  handleAddUser,
  setShowSelectRoute,
}) => (
  <BottomSheetView style={styles.contentContainer}>
    <YStack px="$4" gap={"$4"} pb={"$2"}>
      <BottomSheetHeader
        title={"Add Guardians"}
        members={members}
        expandSheet={expandSheet}
      />
    </YStack>

    <YStack
      width="95%"
      px="$2"
      gap="$2"
      justify={"space-between"}
      height={"82%"}
    >
      <YStack>
        <Input
          value={searchTerm}
          onChangeText={setSearchTerm}
          placeholder="Search by username"
          width="100%"
          alignSelf="center"
          marginVertical="$4"
          marginTop="$8"
          size={"$7"}
          fontWeight="700"
        />

        <YStack gap="$3" flexWrap="wrap">
          {users.map((user, idx) => (
            <XStack
              key={idx}
              justify="space-between"
              alignItems="center"
              bg="$white2"
              py="$2"
              pr="$4"
              pl="$2"
              rounded="$6"
              borderColor="$white5"
              borderWidth="2"
            >
              <XStack flex={1} gap="$4" alignItems="center" width={80}>
                <Avatar circular size="$6">
                  <Avatar.Image
                    accessibilityLabel={user.name}
                    src={members[idx].avatar}
                  />
                </Avatar>
                <Text fontSize="$7" lineHeight={20}>
                  <Text fontWeight="600">
                    {user.name?.split(" ")[0] ?? "Unnamed"}
                  </Text>
                  {user.name && user.name.split(" ").length > 1 && (
                    <>
                      {"\n"}
                      <Text fontWeight="400">
                        {user.name.split(" ").slice(1).join(" ")}
                      </Text>
                    </>
                  )}
                </Text>
              </XStack>
              <Pressable onPress={() => handleAddUser(user.username)}>
                <UserRoundPlus size={"$2"} />
              </Pressable>
            </XStack>
          ))}
        </YStack>
      </YStack>

      <PrimaryBtn
        onPress={() => setShowSelectRoute(true)}
        iconAfter={ChevronRight}
        theme="gray"
        marginTop="$4"
      >
        Next
      </PrimaryBtn>
    </YStack>
  </BottomSheetView>
);

export default AddGuardianBottomView;

const styles = StyleSheet.create({
  contentContainer: {
    flex: 1,
    alignItems: "center",
  },
});

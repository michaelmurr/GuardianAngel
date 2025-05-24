import { Plus } from "@tamagui/lucide-icons";
import { Avatar, H2, H3, H4, XStack, YStack, ZStack } from "tamagui";

const BottomSheetHeader = ({ title, members, expandSheet }) => {
  return (
    <YStack>
      <XStack width="100%" justify="space-between" alignItems="center" gap="$2">
        <H4 fontWeight="700">{title}</H4>
        <Plus onPress={expandSheet} size="$3" />
      </XStack>
      <ZStack pt="$6">
        {members.map((member, id) => {
          return (
            <Avatar circular size="$6" key={id} left={35 * id}>
              <Avatar.Image accessibilityLabel={id} src={member.avatar} />
            </Avatar>
          );
        })}
      </ZStack>
    </YStack>
  );
};

export default BottomSheetHeader;

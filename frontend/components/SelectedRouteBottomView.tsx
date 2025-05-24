import { BottomSheetView } from "@gorhom/bottom-sheet";
import { ChevronDown, ChevronLeft, MapPin } from "@tamagui/lucide-icons";
import { API_URL } from "constants/Key";
import { StyleSheet } from "react-native";
import { Input, XStack, YStack } from "tamagui";
import BottomSheetHeader from "./BottomSheetHeader";
import { PrimaryBtn } from "./PrimaryBtn";

const SelectedRouteBottomView = ({
  expandSheet,
  members,
  street,
  setStreet,
  housenr,
  setHousenr,
  city,
  setCity,
  postalcode,
  setPostalcode,
  setShowSelectRoute,
  setDestination,
  collapseSheet,
  getToken,
}) => {
  const submitRoute = async () => {
    const token = await getToken();

    const res = await fetch(`${API_URL}/routes/coordinates`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        house_number: housenr,
        street,
        city,
        postal_code: postalcode,
      }),
    });
    const json = await res.json();
    console.log(json);
    setDestination(json);
    collapseSheet();
  };
  return (
    <BottomSheetView style={styles.contentContainer}>
      <YStack px="$4" gap={"$4"} pb={"$2"}>
        <BottomSheetHeader
          title={"Select your destination"}
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
        <YStack gap={"$2"} py={"$6"}>
          <XStack justify={"space-between"} mt="$4">
            <Input
              value={street}
              onChangeText={setStreet}
              placeholder="Street"
              alignSelf="center"
              width={"70%"}
              width="68%"
              size={"$7"}
              fontWeight="700"
            />
            <Input
              value={housenr}
              onChangeText={setHousenr}
              placeholder="Housenr."
              alignSelf="center"
              width={"29%"}
              size={"$7"}
              fontWeight="700"
            />
          </XStack>
          <Input
            value={city}
            onChangeText={setCity}
            placeholder="City"
            width="100%"
            alignSelf="center"
            size={"$7"}
            marginTop="$1.5"
            fontWeight="700"
          />
          <Input
            value={postalcode}
            onChangeText={setPostalcode}
            placeholder="Postal Code"
            width="100%"
            alignSelf="center"
            size={"$7"}
            marginTop="$1.5"
            fontWeight="700"
          />
        </YStack>
        <YStack gap="$2">
          <PrimaryBtn
            onPress={async () => submitRoute()}
            icon={MapPin}
            theme="gray"
            marginTop="$4"
          >
            Start
          </PrimaryBtn>
          <PrimaryBtn
            onPress={() => setShowSelectRoute(false)}
            icon={ChevronLeft}
            theme="gray"
            marginTop="$4"
          >
            Back
          </PrimaryBtn>
        </YStack>
      </YStack>
    </BottomSheetView>
  );
};

export default SelectedRouteBottomView;

const styles = StyleSheet.create({
  contentContainer: {
    flex: 1,
    alignItems: "center",
  },
});

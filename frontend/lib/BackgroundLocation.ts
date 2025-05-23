import { NativeModules } from "react-native";

const { BackgroundLocation } = NativeModules;

export default {
  startTracking: () => BackgroundLocation.startTracking(),
};

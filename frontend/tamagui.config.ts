import { defaultConfig } from "@tamagui/config/v4";
import { createTamagui } from "tamagui";

const customConfig = {
  ...defaultConfig,
  themes: {
    ...defaultConfig.themes,
    light: {
      ...defaultConfig.themes.light,
      background: "white", // Override default background
    },
  },
};

export const config = createTamagui(customConfig);

export default config;

export type Conf = typeof config;

declare module "tamagui" {
  interface TamaguiCustomConfig extends Conf {}
}

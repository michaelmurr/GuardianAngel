import React from "react";
import { Button, ButtonProps } from "tamagui";

interface PrimaryBtnProps {
  children: string;
  props?: ButtonProps;
}

export const PrimaryBtn = ({ children, onPress, icon, iconAfter }) => {
  return (
    <Button
      size="$6"
      onPress={onPress}
      fontWeight={"700"}
      bg={"black"}
      color="white"
      fontSize={"$8"}
      pressStyle={{
        backgroundColor: "black", // Change splash/press background
        opacity: 0.8, // Optional: Add some visual feedback
      }}
    >
      {children}
    </Button>
  );
};

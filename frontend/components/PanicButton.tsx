// components/PanicButton.tsx
import React from "react";
import { Text, TouchableOpacity, StyleSheet } from "react-native";

type PanicButtonProps = {
  onPress: () => void;
};

const PanicButton: React.FC<PanicButtonProps> = ({ onPress }) => (
  <TouchableOpacity style={styles.panicButton} onPress={onPress}>
    <Text style={styles.panicButtonText}>PANIC</Text>
  </TouchableOpacity>
);

const styles = StyleSheet.create({
  panicButton: {
    position: "absolute",
    bottom: 20,
    right: 20,
    backgroundColor: "red",
    padding: 20,
    borderRadius: 50,
    zIndex: 2,
  },
  panicButtonText: {
    color: "white",
    fontWeight: "bold",
  },
});

export default PanicButton;

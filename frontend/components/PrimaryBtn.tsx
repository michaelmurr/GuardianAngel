import React from 'react';
import { Button, ButtonProps } from 'tamagui';

interface PrimaryBtnProps {
        children: string;
        props?: ButtonProps;
}

export const PrimaryBtn = ({ children, onPress }) => {
        return (
                <Button onPress={onPress} fontWeight={"700"} bg={"black"} color='white' >{children}</Button>
        )
}

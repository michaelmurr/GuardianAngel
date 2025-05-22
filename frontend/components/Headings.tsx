import React from 'react';
import { H1, H2 } from 'tamagui';

export const HeadingH1 = ({ children }) => {
        return (
                <H1 fontWeight={"700"}>{children}</H1>
        )
}

export const HeadingH2 = ({ children }) => {
        return (
                <H2 fontWeight={"700"} color={"$color"} >{children}</H2>
        )
}
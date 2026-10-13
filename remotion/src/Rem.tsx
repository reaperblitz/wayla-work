import React from "react";
import {Composition} from "remotion";
import {WaylaShort, WAYLA_SHORT_DEFAULT_PROPS} from "./WaylaShort";

export const Rem: React.FC = () => {
  return (
    <>
      <Composition
        id="WaylaShort"
        component={WaylaShort}
        durationInFrames={450}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={WAYLA_SHORT_DEFAULT_PROPS}
      />
    </>
  );
};

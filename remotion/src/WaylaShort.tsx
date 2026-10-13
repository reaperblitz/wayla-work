import React from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

export type WaylaShortProps = {
  title: string;
  hook: string;
  caption: string;
  taskStem: string;
};

export const WAYLA_SHORT_DEFAULT_PROPS: WaylaShortProps = {
  title: "Wayla Science Lab",
  hook: "NEW SHORT",
  caption: "Shot by the queue runner",
  taskStem: "sample-task",
};

const clampText = (s: string, n: number) =>
  s.length > n ? s.slice(0, n - 1).trimEnd() + "…" : s;

export const WaylaShort: React.FC<WaylaShortProps> = ({
  title,
  hook,
  caption,
  taskStem,
}) => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();

  const hookScale = spring({frame, fps, config: {damping: 12, stiffness: 160}});
  const hookOpacity = interpolate(frame, [0, 12], [0, 1], {
    extrapolateRight: "clamp",
  });
  const titleY = interpolate(frame, [8, 30], [60, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const accentW = interpolate(frame, [0, durationInFrames], [0, 1080], {
    extrapolateRight: "clamp",
  });
  const pulse = 1 + 0.03 * Math.sin((frame / fps) * Math.PI * 2);

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#0b0b12",
        fontFamily: "Arial, Helvetica, sans-serif",
      }}
    >
      {/* top brand bar */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          right: 0,
          height: 150,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <div
          style={{
            color: "#ffffff",
            opacity: 0.85,
            fontSize: 44,
            fontWeight: 800,
            letterSpacing: 6,
          }}
        >
          WAYLA
        </div>
      </div>

      {/* animated accent line */}
      <div
        style={{
          position: "absolute",
          top: 150,
          left: 0,
          height: 10,
          width: accentW,
          backgroundColor: "#ff3d5a",
        }}
      />

      {/* hook pill */}
      <div
        style={{
          position: "absolute",
          top: 260,
          left: 0,
          right: 0,
          display: "flex",
          justifyContent: "center",
          opacity: hookOpacity,
          transform: `scale(${hookScale})`,
        }}
      >
        <div
          style={{
            backgroundColor: "#ff3d5a",
            color: "#fff",
            fontSize: 52,
            fontWeight: 900,
            padding: "18px 46px",
            borderRadius: 999,
            maxWidth: 920,
            textAlign: "center",
          }}
        >
          {clampText(hook || "NEW SHORT", 60)}
        </div>
      </div>

      {/* title block */}
      <div
        style={{
          position: "absolute",
          top: 560,
          left: 80,
          right: 80,
          transform: `translateY(${titleY}px) scale(${pulse})`,
        }}
      >
        <div
          style={{
            color: "#ffffff",
            fontSize: 96,
            fontWeight: 900,
            lineHeight: 1.08,
            textAlign: "center",
          }}
        >
          {clampText(title || "Wayla Science Lab", 90)}
        </div>
      </div>

      {/* caption block */}
      <div
        style={{
          position: "absolute",
          top: 1180,
          left: 90,
          right: 90,
          display: "flex",
          justifyContent: "center",
        }}
      >
        <div
          style={{
            color: "#d7d7e0",
            fontSize: 48,
            lineHeight: 1.3,
            textAlign: "center",
            maxWidth: 900,
          }}
        >
          {clampText(caption || "", 160)}
        </div>
      </div>

      {/* progress bar */}
      <div
        style={{
          position: "absolute",
          left: 80,
          right: 80,
          bottom: 220,
          height: 14,
          borderRadius: 7,
          backgroundColor: "rgba(255,255,255,0.18)",
          overflow: "hidden",
        }}
      >
        <div
          style={{
            height: "100%",
            width: `${(frame / Math.max(durationInFrames - 1, 1)) * 100}%`,
            backgroundColor: "#ff3d5a",
          }}
        />
      </div>

      {/* footer */}
      <div
        style={{
          position: "absolute",
          left: 0,
          right: 0,
          bottom: 90,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 8,
        }}
      >
        <div style={{color: "#ffffff", fontSize: 40, fontWeight: 800}}>
          @waylasciencelab357
        </div>
        <div style={{color: "rgba(255,255,255,0.55)", fontSize: 30}}>
          {clampText(taskStem || "", 60)} · 1080x1920
        </div>
      </div>
    </AbsoluteFill>
  );
};

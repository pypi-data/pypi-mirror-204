import type { AvailablePlugins, IMakePlugin } from "@/schema/plugins";

export const reactPluginSettings: IMakePlugin<AvailablePlugins>[] = [
  {
    type: "meta",
    props: {
      nodeConstraint: "singleNode",
      renderInfo: {
        w: 400,
        h: 400,
        offsetY: 48,
        src: "https://ailab-huawei-cdn.nolibox.com/upload/images/0ec1b08f9c3e4ef4813ecb80bebf3b42.png",
        pivot: "rt",
        follow: true,
      },
      pluginInfo: {},
    },
  },
  {
    type: "settings",
    props: {
      nodeConstraint: "none",
      renderInfo: {
        w: 300,
        h: 400,
        src: "https://ailab-huawei-cdn.nolibox.com/upload/images/49223052f17f4f249c56ba00f43b3043.png",
        pivot: "rt",
        follow: false,
      },
      pluginInfo: {},
    },
  },
  {
    type: "project",
    props: {
      nodeConstraint: "none",
      renderInfo: {
        w: 300,
        h: 400,
        offsetY: 64,
        src: "https://ailab-huawei-cdn.nolibox.com/upload/images/255c1c20b5754815b759969218f8a87c.png",
        pivot: "rt",
        follow: false,
      },
      pluginInfo: {},
    },
  },
  {
    type: "add",
    props: {
      p: "14px",
      nodeConstraint: "none",
      renderInfo: {
        w: 300,
        h: 225,
        offsetY: 120,
        src: "https://ailab-huawei-cdn.nolibox.com/upload/images/81a82eca03224bc2bb8de65c08f2f48a.png",
        pivot: "rt",
        follow: false,
      },
      pluginInfo: {},
    },
  },
  {
    type: "arrange",
    props: {
      nodeConstraint: "multiNode",
      renderInfo: {
        w: 0,
        h: 0,
        offsetY: 48,
        src: "https://ailab-huawei-cdn.nolibox.com/upload/images/7fcc3fb8a25248b0a1f2ca68b0c975f4.png",
        pivot: "rt",
        follow: true,
      },
      pluginInfo: {},
      noExpand: true,
    },
  },
  {
    type: "undo",
    props: {
      p: "14px",
      nodeConstraint: "none",
      renderInfo: {
        w: 0,
        h: 0,
        offsetX: -28,
        src: "https://ailab-huawei-cdn.nolibox.com/upload/images/069122c037d34d97ba10157438af131b.png",
        pivot: "top",
      },
      pluginInfo: {},
      noExpand: true,
    },
  },
  {
    type: "redo",
    props: {
      p: "14px",
      nodeConstraint: "none",
      renderInfo: {
        w: 0,
        h: 0,
        offsetX: 28,
        src: "https://ailab-huawei-cdn.nolibox.com/upload/images/4c0b2343838344fdb574520006aa83c9.png",
        pivot: "top",
      },
      pluginInfo: {},
      noExpand: true,
    },
  },
  {
    type: "download",
    props: {
      nodeConstraint: "anyNode",
      renderInfo: {
        w: 240,
        h: 230,
        offsetY: -48,
        src: "https://ailab-huawei-cdn.nolibox.com/upload/images/d871d80a875146fa8aabc09fbbdef47e.png",
        pivot: "rb",
        follow: true,
      },
      pluginInfo: {},
    },
  },
  {
    type: "delete",
    props: {
      nodeConstraint: "anyNode",
      renderInfo: {
        w: 0,
        h: 0,
        offsetY: -48,
        src: "https://ailab-huawei-cdn.nolibox.com/upload/images/384b2261faa748e6b57e14e697e19520.png",
        pivot: "lb",
        follow: true,
      },
      pluginInfo: {},
      noExpand: true,
    },
  },
  {
    type: "textEditor",
    props: {
      p: "13px",
      nodeConstraint: "text",
      renderInfo: {
        w: 300,
        h: 400,
        src: "https://ailab-huawei-cdn.nolibox.com/upload/images/06dc5af9d77944c8ae06d1ae1124b6a2.png",
        pivot: "right",
        follow: true,
      },
      pluginInfo: {},
    },
  },
  {
    type: "groupEditor",
    props: {
      // p: "13px",
      nodeConstraint: "group",
      renderInfo: {
        w: 0,
        h: 0,
        src: "https://ailab-huawei-cdn.nolibox.com/upload/images/b767f4a99956498a922470174a2051df.png",
        pivot: "rt",
        follow: true,
      },
      pluginInfo: {},
      noExpand: true,
    },
  },
  {
    type: "multiEditor",
    props: {
      // p: "13px",
      nodeConstraint: "multiNode",
      renderInfo: {
        w: 0,
        h: 0,
        src: "https://ailab-huawei-cdn.nolibox.com/upload/images/669c405bee944a9a91fc4aa68f858cc3.png",
        pivot: "rt",
        follow: true,
      },
      pluginInfo: {},
      noExpand: true,
    },
  },
  {
    type: "brush",
    props: {
      p: "0px",
      pl: "10px",
      pr: "7px",
      nodeConstraint: "none",
      renderInfo: {
        w: 300,
        h: 220,
        offsetY: 176,
        src: "https://ailab-huawei-cdn.nolibox.com/upload/static/brush.svg",
        pivot: "rt",
        follow: false,
      },
      pluginInfo: {},
    },
  },
  {
    type: "wiki",
    props: {
      nodeConstraint: "none",
      renderInfo: {
        w: 0,
        h: 0,
        src: "https://ailab-huawei-cdn.nolibox.com/upload/images/7ca6f41cad574f35ab117d6cfbe53be4.png",
        pivot: "rb",
      },
      pluginInfo: {},
      noExpand: true,
    },
  },
  {
    type: "email",
    props: {
      nodeConstraint: "none",
      renderInfo: {
        w: 0,
        h: 0,
        offsetX: -120,
        src: "https://ailab-huawei-cdn.nolibox.com/upload/images/7ff42ebb21664a9abb55331463951126.png",
        pivot: "rb",
      },
      pluginInfo: {},
      noExpand: true,
    },
  },
  {
    type: "github",
    props: {
      nodeConstraint: "none",
      renderInfo: {
        w: 0,
        h: 0,
        offsetX: -64,
        src: "https://ailab-huawei-cdn.nolibox.com/upload/images/4fb8d24d515744f6ac6836b3ba12a649.png",
        pivot: "rb",
      },
      pluginInfo: {},
      noExpand: true,
    },
  },
];

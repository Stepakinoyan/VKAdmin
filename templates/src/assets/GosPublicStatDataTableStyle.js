export const GosPublicStatDataTableStyle = {
    root: ({ props }) => ({
      class: [
        "relative",
        {
          "flex flex-col": props.scrollable && props.scrollHeight === "flex",
        },
        { "h-full": props.scrollable && props.scrollHeight === "flex" },
        "rounded-lg",
      ],
    }),
    loadingoverlay: {
      class: [
        "absolute",
        "top-0 left-0",
        "z-20",
        "flex items-center justify-center",
        "w-full h-full",
        "bg-surface-100/40",
        "transition duration-200",
        "rounded-lg",
      ],
    },
    wrapper: ({ props }) => ({
      class: [
        {
          relative: props.scrollable,
          "flex flex-col grow": props.scrollable && props.scrollHeight === "flex",
        },
        { "h-full": props.scrollable && props.scrollHeight === "flex" },
        "rounded-lg",
      ],
    }),
    header: ({ props }) => ({
      class: [
        "font-bold",
        props.showGridlines ? "border-x border-t border-b-0" : "border-y border-x-0",
        "p-4",
        "bg-surface-50 dark:bg-surface-800",
        "border-gosuslugi-border",
        "text-surface-700 dark:text-white/80",
        "rounded-t-lg",
      ],
    }),
    table: {
      class: [
        "w-full",
        "border-spacing-0",
        "border-separate",
        "rounded-lg",
      ],
    },
    tbody: ({ instance, context }) => ({
      class: [
        {
          "sticky z-20": instance.frozenRow && context.scrollable,
        },
        "bg-surface-50 dark:bg-surface-800 rounded-lg",
      ],
    }),
    footer: {
      class: [
        "font-bold",
        "border-t-0 border-b border-x-0",
        "p-4",
        "bg-surface-50 dark:bg-surface-800",
        "border-gosuslugi-border",
        "text-surface-700 dark:text-white/80",
        "rounded-b-lg",
      ],
    },
    filteroverlay: {
      class: [
        "absolute top-0 left-0",
        "border-0 dark:border",
        "rounded-md",
        "shadow-md",
        "min-w-[12.5rem]",
        "bg-surface-0 dark:bg-surface-800",
        "text-surface-800 dark:text-white/80",
        "rounded-lg",
      ],
    },
};
<template>
  <Password
    placeholder="Пароль"
    :feedback="false"
    :pt="{
      input: {
        root: ({ props, context, parent }) => {
          var _a, _b, _c;
          return {
            class: [
              // Font
              'leading-[normal]',
              // Flex
              {
                'flex-1 w-[1%]': parent.instance.$name == 'InputGroup',
              },
              // Spacing
              'm-0',
              {
                'px-4 py-4': props.size == 'large',
                'px-2 py-2': props.size == 'small',
                'p-3': props.size == null,
              },
              'w-full',
              // Shape
              { 'rounded-md': parent.instance.$name !== 'InputGroup' },
              {
                'first:rounded-l-md rounded-none last:rounded-r-md':
                  parent.instance.$name == 'InputGroup',
              },
              {
                'border-0 border-y border-l last:border-r':
                  parent.instance.$name == 'InputGroup',
              },
              {
                'first:ml-0 -ml-px':
                  parent.instance.$name == 'InputGroup' && !props.showButtons,
              },
              // Colors
              'text-surface-600 dark:text-surface-200',
              'placeholder:text-gray-500',
              'bg-surface-0 dark:bg-surface-900',
              'border',
              { 'border-gosuslugi-border': !parent.props.invalid },
              // Invalid State
              {
                'border-red-500 dark:border-red-400': parent.props.invalid,
              },
            ],
          };
        },
      },
    }"
  />
</template>

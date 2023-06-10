from tree_sitter import Language

Language.build_library(
  # so文件保存位置
  '/root/project/codex/method/ptuning/tree_sitter_utils/tree_sitter_build/my-languages.so',

  # vendor文件下git clone的仓库
  [
    '/root/project/codex/method/ptuning/tree_sitter_utils/vendor/tree-sitter-python',
  ]
)


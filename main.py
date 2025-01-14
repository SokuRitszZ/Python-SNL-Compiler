import sys, os
import grammar.LL1 as grammar
import morer.morer as morer 
import analyzer.semantic as analyser
from util.logger import log, set_debug
from formula.formula import generater

def __get_token_and_tree(snlText: str):
  token = ''
  tree = ''
  return token, tree;

if __name__ == '__main__':
  # run()
  # grammar.run();
  args = sys.argv
  if len(args) < 2:
    print('使用方法: python main.py <文件名>.snl [--debug] [-o <输出文件名>]')
    os._exit(1)

  if '--debug' in args:
    set_debug()

  output = 'dist/a.out'
  if '-o' in args:
    try:
      output = 'dist/' + args[args.index('-o') + 1]
    except Exception:
      print('使用方法: python main.py <文件名>.snl [--debug] [-o <输出文件名>]')
      os._exit(1)

  fileName = args[1]
  snlText = ''
  with open(fileName, encoding='utf-8') as file:
    snlText = file.read()

  # 运行 词法分析器 根据SNLText 获取 TokenList
  tokenList = morer.run(snlText)

  log('\n'.join(map(lambda x: str(x), tokenList)))

  # 运行 语法分析器 根据TokenList 获取 AST
  tree = grammar.run(tokenList)
  
  # 通过 AST 和 Tokens 获取符号表信息、分析语义
  _analyser = analyser.Analyzer(tokenList, tree)
  _analyser.analyze()

  # TODO 中间代码优化
  _generator = generater(tree)
  formula_list = _generator.scan()
  formula_list.show(output)

  print('结果已生成在 dist 目录下')

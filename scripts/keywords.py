import sys


def main(output_filepath):
    filepath = "./config/keywords-list.txt"
    try:
        with (
            open(filepath, "r", encoding="utf-8") as fin,
            open(output_filepath, "w", encoding="utf-8") as fout,
        ):
            fout.write("payload:\n")
            for line in fin:
                line = line.strip()
                if line:
                    # 将"DOMAIN-KEYWORD"规则写入到"keywords.txt"文件中
                    fout.write(f"  - DOMAIN-KEYWORD,{line}\n")
    except FileNotFoundError:
        print(f"文件 '{filepath}' 未找到。")


if __name__ == "__main__":
    main(sys.argv[1])


#? 用于生成 keywords.txt 规则，使用 DOMAIN-KEYWORD 代替多个 DOMAIN-SUFFIX 规则
#? 我这里没有管过滤问题，这个交给 AdGuard Home 来处理吧

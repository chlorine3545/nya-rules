import os
import sys
import logging
import shutil
from typing import Set
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def read_keywords(config_path: str = "./config/keywords-list.txt") -> Set[str]:
    """
    从配置文件中读取关键词列表

    Args:
        config_path: 关键词配置文件路径

    Returns:
        包含所有关键词的集合

    Raises:
        FileNotFoundError: 当配置文件不存在时
    """
    keywords = set()
    config_path = Path(config_path)

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    keywords.add(line)
        logger.info(f"成功从 {config_path} 读取了 {len(keywords)} 个关键词")
        return keywords
    except FileNotFoundError:
        logger.error(f"配置文件 '{config_path}' 未找到")
        raise
    except UnicodeDecodeError:
        logger.error(f"配置文件 '{config_path}' 编码错误，请确保使用 UTF-8 编码")
        raise
    except Exception as e:
        logger.error(f"读取配置文件时发生未知错误: {e}")
        raise


def simplify_file(filepath: str, keywords: Set[str]) -> None:
    """
    根据关键词过滤文件内容

    Args:
        filepath: 需要处理的文件路径
        keywords: 关键词集合

    Raises:
        FileNotFoundError: 当文件不存在时
        OSError: 当文件操作失败时
    """
    filepath = Path(filepath)
    backup_path = filepath.with_suffix(filepath.suffix + ".bak")
    temp_path = filepath.with_suffix(filepath.suffix + ".tmp")

    try:
        # 创建备份
        shutil.copy2(filepath, backup_path)
        logger.info(f"已创建备份文件: {backup_path}")

        # 处理文件
        with (
            open(filepath, "r", encoding="utf-8") as f_in,
            open(temp_path, "w", encoding="utf-8") as f_out,
        ):
            filtered_count = 0
            total_count = 0

            for line in f_in:
                total_count += 1
                if not any(keyword in line for keyword in keywords):
                    f_out.write(line)
                else:
                    filtered_count += 1

        # 原子性替换文件
        os.replace(temp_path, filepath)
        logger.info(f"文件处理完成: 总行数 {total_count}, 过滤行数 {filtered_count}")

        # 处理成功后删除备份
        backup_path.unlink()
        logger.info("处理成功，已删除备份文件")

    except FileNotFoundError:
        logger.error(f"文件 '{filepath}' 未找到")
        raise
    except UnicodeDecodeError:
        logger.error(f"文件 '{filepath}' 编码错误，请确保使用 UTF-8 编码")
        if temp_path.exists():
            temp_path.unlink()
        raise
    except Exception as e:
        logger.error(f"处理文件 '{filepath}' 时发生错误: {e}")
        # 发生错误时恢复备份
        if backup_path.exists():
            shutil.copy2(backup_path, filepath)
            logger.info("已从备份恢复原文件")
        if temp_path.exists():
            temp_path.unlink()
        raise


def main() -> None:
    """
    主函数，处理命令行参数并执行文件简化操作
    """
    try:
        if len(sys.argv) != 2:
            logger.error("用法: python simplify.py <输入文件路径>")
            sys.exit(1)

        filepath = sys.argv[1]
        keywords = read_keywords()

        if not keywords:
            logger.error("未读取到任何关键词，操作取消")
            sys.exit(1)

        simplify_file(filepath, keywords)

    except Exception as e:
        logger.error(f"程序执行失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

# ? 用来对下载的 gfw.txt 文件进行过滤，去除一些无用的规则。这些规则将由我的 DOMAIN-KEYWORD 规则替代。

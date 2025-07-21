# 项目构建 Makefile

# 构建目标目录
DIST_DIR := dist
INTEGRATION := $(DIST_DIR)/app

# 默认目标：构建前端、后端并集成
all: build-web build-backend integration

# 构建前端应用
build-web:
	@if [ -d "web" ]; then \
		echo "🚀 开始构建前端应用..."; \
		chmod +x web/build.sh; \
		cd web && ./build.sh; \
		echo "✅ 前端应用构建完成!"; \
	else \
		echo "⚠️  未找到 web 目录，跳过前端构建"; \
	fi

tar_backend:
	@cd dist/app && tar -zcvf backend.tar.gz *

# 构建后端应用
build-backend:
	@if [ -d "backend" ]; then \
		echo "🚀 开始构建后端应用..."; \
		chmod +x backend/build.sh; \
		cd backend && ./build.sh; \
		echo "✅ 后端应用构建完成!"; \
	else \
		echo "⚠️  未找到 backend 目录，跳过后端构建"; \
	fi

# 清理构建产物
clean:
	@echo "🧹 清理构建结果..."
	@rm -rf $(DIST_DIR)
	@if [ -d "web" ]; then cd web && ./build.sh clean || true; fi
	@if [ -d "backend" ]; then cd backend && ./build.sh clean || true; fi
	@echo "✅ 清理完成!"

# 构建成品目录结构并集成文件
integration:
	@echo "📦 整合构建产物..."
	@mkdir -p $(INTEGRATION)/app
	@mkdir -p $(INTEGRATION)/logs
	@mkdir -p $(INTEGRATION)/tmp
	@mkdir -p $(INTEGRATION)/config
	@mkdir -p $(INTEGRATION)/data
# 	@if [ -d "dist/web" ]; then \
# 		cp -r dist/web $(INTEGRATION)/app/web; \
# 	else \
# 		echo "⚠️  未找到 web 构建产物，跳过复制"; \
# 	fi
	@if [ -d "dist/backend" ]; then \
		cp -r dist/backend/main.dist $(INTEGRATION)/app/bin; \
	else \
		echo "⚠️  未找到 backend 构建产物，跳过复制"; \
	fi
	@echo "✅ 构建产物整合完成!"

# 帮助信息
help:
	@echo ""
	@echo "可用命令:"
	@echo "  make all            - 构建前端、后端并集成到 dist/"
	@echo "  make build-web      - 仅构建前端应用"
	@echo "  make build-backend  - 仅构建后端应用"
	@echo "  make integration    - 整合构建结果"
	@echo "  make tar_backend    - 压缩后端制品结构"
	@echo "  make clean          - 清理构建结果"
	@echo "  make help           - 显示此帮助信息"
	@echo ""

.PHONY: all build-web build-backend clean integration help
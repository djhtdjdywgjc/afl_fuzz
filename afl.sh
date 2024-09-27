#!/bin/bash
sudo apt-get update
sudo apt-get install -y build-essential python3-dev automake git flex bison libglib2.0-dev libpixman-1-dev python3-setuptools
sudo apt-get install -y lld-14 llvm-14 llvm-14-dev clang-14 || sudo apt-get install -y lld llvm llvm-dev clang 
sudo apt-get install -y gcc-$(gcc --version|head -n1|sed 's/.* //'|sed 's/\..*//')-plugin-dev libstdc++-$(gcc --version|head -n1|sed 's/.* //'|sed 's/\..*//')-dev

# 设置 llvm-config 版本
export LLVM_CONFIG="llvm-config-14"
echo "Using LLVM config: $LLVM_CONFIG"

# 克隆 AFL++ 仓库
echo "Cloning AFL++ repository..."
git clone https://github.com/AFLplusplus/AFLplusplus.git
cd AFLplusplus

# 编译 AFL++
echo "Building AFL++..."
sudo make distrib

# 安装 AFL++
echo "Installing AFL++..."
sudo make install

# 检查是否安装成功
echo "Verifying AFL++ installation..."
if command -v afl-fuzz &> /dev/null
then
    echo "AFL++ installation successful!"
    echo "AFL++ version:"
    afl-fuzz -h | head -n 1
else
    echo "AFL++ installation failed. Please check the output for errors."
    exit 1
fi

# 提示用户可以开始使用 AFL++
echo "AFL++ environment setup complete. You can now start fuzzing using afl-fuzz."

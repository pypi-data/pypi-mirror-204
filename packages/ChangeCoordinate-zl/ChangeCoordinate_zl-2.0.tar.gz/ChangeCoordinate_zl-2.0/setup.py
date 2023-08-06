#autor:pianshilengyubing（xiaohuangya）
#time: 2021/5/29 20:54
import setuptools
setuptools.setup(
	name="ChangeCoordinate_zl",
	version="2.0",
	author="pianshilengyubing",
	author_email="1010221702@qq.com",
	description="基于ChangeCoordinate添加高德与wgs84相互转换等",
	long_description="基于ChangeCoordinate添加高德与wgs84相互转换等",
	long_description_content_type="text/markdown",  # 所需要的依赖
	install_requires=[],  # 比如["flask>=0.10"]
	url="https://space.bilibili.com/31106656",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
)
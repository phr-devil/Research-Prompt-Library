# PyTorch 算法合同测试｜接入实际项目

**用途**：把 [test_algorithm_contract.py](test_algorithm_contract.py) 复制到目标算法仓库 `tests/`，由 WorkBuddy/Codex 在**现有 PyTorch 环境**适配实际模型与**训练/开发数据的最小真实 batch**。不是在提示词库中替你运行模型；不新增 GPU、安装依赖或正式训练许可。

## ① 最小适配（由 Agent 按真实文件路径改写）

在目标项目根目录建立 `algorithm_contract_adapter.py`（示例接口，**下列函数不是可直接运行的项目实现**）：

~~~python
# 使用目标项目已有模型/加载器替换名称与参数；batch 及模型留在 CPU。
def make_case():
    model = ExistingModel(existing_config).cpu()
    batch = next(iter(existing_train_loader()))  # 真实 train/开发样本，绝不读 holdout
    return model, move_batch_to_cpu(batch)

def predict(model, batch):
    return model(batch["x"], mask=batch["mask"])  # 按实际 forward 签名适配

def loss(pred, batch):
    return existing_loss(pred, batch["y"])

def assert_contract(pred, batch):
    assert pred.shape == batch["y"].shape
    assert pred.isfinite().all()
    # 依据实际任务再断言 dtype、单位、有效 mask、时间索引与预测 horizon

key_parameter_names = ["my_new_module.weight"]  # 改为真实新增模块参数名
~~~

四个接口 `make_case / predict / loss / assert_contract` **必须实现**。`make_case` 每次返回**新模型与真实 CPU batch**；如是分类模型，按 `[B,C]` logits 与 `[B]` target 合法关系断言，不能照抄上方 shape 等式。若需要自定义 optimizer，提供 `make_optimizer(model)`；新增模块必须指定其真实 `key_parameter_names`，确认梯度进入研究机制。

按本次科研任务可选增加：`loss_examples()`（独立手算 Tensor 对）；`reference_prediction(model,batch)`（独立实现，参考输出）；`gradcheck_case()` 返回 `(op, (float64_requires_grad_inputs,...))`；`deployment_batch()`（**不含目标或未来值**）；`invariance_cases()`（`[(name,batch_a,batch_b),...]`，仅放物理/时序上真正应相等的输出）。缺少的可选检查记 **SKIP ≠ VERIFIED**，不得向论文汇报已验证。

## ② 运行与验收

~~~bash
# 从目标算法仓库根目录执行（在本机现有的 PyTorch CPU 环境）
ALGORITHM_CONTRACT_ADAPTER=algorithm_contract_adapter python -m unittest -v tests.test_algorithm_contract
# Windows PowerShell：
# $env:ALGORITHM_CONTRACT_ADAPTER="algorithm_contract_adapter"
# python -m unittest -v tests.test_algorithm_contract
~~~

没有适配器会**失败退出**，不会虚构 PASS。对已有测试框架（pytest 等）可以只移植对应行为，不强制换环境。主要输出：实际通过/失败/SKIP 的测试、执行命令、Git SHA、项目数据/协议版本和关联 Run；可以增量记录到既有 STATE/RUNS。测试本身不证明数据来自真实物理传感器——需要指向数据文件和元信息。**工程测试通过 ≠ 算法优于强基线 ≠ 机制/论文主张成立**。

只把已知确定行为做成强制断言；研究假设增益与泛化由同一评价器上的实际实验确认。多项 Loss、非平滑算子、混合精度和缓存状态要按实际数学定义分别审查；`gradcheck` 仅适用于可微且避开不光滑点的 double 小样例。

参考：[PyTorch gradcheck](https://docs.pytorch.org/docs/stable/generated/torch.autograd.gradcheck.html) · [Hugging Face Writing model tests](https://huggingface.co/docs/transformers/en/testing)。

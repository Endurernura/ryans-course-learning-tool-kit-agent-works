# Ryan's Course Learning Tool Kit: Agent Works

这是我个人使用的课内学习工具包的 Agent 调度部分。它把课程材料归档、录音与课件核对、考点查漏、复习材料撰写、练习题制作和反馈修订串成可重复使用的工作流程。

## 课内材料撰写

[Skill 入口](.agents/skills/rw-course-learning-writing/SKILL.md)说明如何判断任务范围并选择下一步。[来源核对](.agents/skills/rw-course-learning-writing/references/evidence-and-coverage.md)、[成稿验收](.agents/skills/rw-course-learning-writing/references/writing-and-validation.md)、[可读性审查](.agents/skills/rw-course-learning-writing/references/readability-review.md)与[反馈迭代](.agents/skills/rw-course-learning-writing/references/revision-loop.md)提供按需查阅的工作方法。

使用时可通过 `$rw-course-learning-writing` 指定该 Skill，同时提供课程材料的位置、期望产物和本轮范围。课程文件、真实录音、题库和个人项目记录由使用者在自己的工作区维护。

## 云端使用

- **Codex Cloud。** 把本仓库加入 Cloud 环境，从包含本仓库的环境新建任务。项目内 `.agents/skills/` 中的 Skill 会随仓库进入任务。也可以把整个 Skill 目录复制到其他目标项目的同一路径，再从该项目新建任务。 [Cloud 环境说明](https://learn.chatgpt.com/docs/environments/cloud-environments)
- **ChatGPT。** 工作区提供 Skill 上传时，将 `rw-course-learning-writing` 目录连同其参考文件打包，在「插件 → Skills → 创建 → 从电脑上传」导入。待检查完成后，在新对话选择该 Skill 并提供练习所需的课程材料。上传和使用权限依所在工作区而定。 [ChatGPT Skills 说明](https://help.openai.com/en/articles/20001066-skills-in-chatgpt)

## 许可

本仓库的原创工作流与说明采用 [知识共享署名-非商业性使用 4.0 国际许可协议（CC BY-NC 4.0）](https://creativecommons.org/licenses/by-nc/4.0/)。许可全文见 [LICENSE](LICENSE)。

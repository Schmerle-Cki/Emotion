<template>
  <el-dialog
        style="text-align: center"
        title="发表"
        :visible.sync="dialogVisible"
        :show-close=false
        :close-on-click-model="false"
        width="80%">
    <el-form label-width="80px">
        <el-form-item label="标题">
            <!--请修改这两行注释中间的代码来输入消息标题-->
            <el-input v-model="title" placeholder="title">title</el-input>
            <!--请修改这两行注释中间的代码来输入消息标题-->
        </el-form-item>
        <el-form-item label="内容">
            <!--请修改这两行注释中间的代码来输入消息内容-->
            <el-input v-model="content" type="textarea" placeholder="message"></el-input>
            <!--请修改这两行注释中间的代码来输入消息内容-->
        </el-form-item>
        <el-form-item label="用户名">
            <!--请修改这两行注释中间的代码来输入用户名-->
            <el-input v-model="state.username"></el-input>
            <!--请修改这两行注释中间的代码来输入用户名-->
            <span v-if="state.username_valid===false" style="color: red">请设置合法用户名!</span>
        </el-form-item>
    </el-form>
    <span slot="footer" class="dialog-footer">
                <!--请修改这两行注释中间的代码来产生相应按钮的点击事件-->
                <el-button v-on:click="withdraw">取 消</el-button>
                <el-button type="primary"
                            v-on:click="ensure"
                            :disabled="state.username_valid===false"
                            >确 定</el-button>
                <!--请修改这两行注释中间的代码来产生相应按钮的点击事件-->
    </span>
  </el-dialog>
</template>

<script>
export default {
  name: "PostDialog",
  props: {
    dialogVisible: {
      type: Boolean,
      default: () => true
    },
    state: {
      type: Object,
      default: () => {
          return {
          username: "",
          username_valid: false
        }
      }
    }
  },
  // 请在下方设计自己的数据结构以及事件函数
  data(){
    return {
      title:"",
      content:"",
      user:this.state.username
    }
  },
  methods: {
    ensure:function(event){
      if(event && this.state.username_valid)
        this.dialogVisible=false
        this.$emit('newMember',
        {title: this.title,
        content:this.content,
        user: this.state.username,
        timestamp: new Date().getTime()})
        this.title=""
        this.content=""
    },
    withdraw:function(event){
      if(event)
        this.dialogVisible=false
        this.$emit('WITHDRAW')
        this.title=""
        this.content=""
    }
  },
  watch: { // 用于实时检测username是否合法
    "state.username": {
      handler(newName) {
        this.state.username_valid = /^[A-Za-z\u4e00-\u9fa5][-A-Za-z0-9\u4e00-\u9fa5_]*$/.test(newName)
      }
    }
  }
}
</script>
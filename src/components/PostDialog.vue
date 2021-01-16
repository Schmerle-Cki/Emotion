<template>
  <el-dialog
        style="text-align: center"
        title="基本信息"
        :visible.sync="dialogVisible"
        :show-close=false
        :close-on-click-model="false"
        width="80%">
		
    <el-form label-width="80px">
        <el-form-item label="用户名">
            <!--请修改这两行注释中间的代码来输入用户名-->
            <el-input v-model="state.username"></el-input>
            <!--请修改这两行注释中间的代码来输入用户名-->
            <span v-if="state.username_valid===false" style="color: red">请设置合法用户名!</span>
        </el-form-item>
		<el-form-item label="性别">
			<el-select v-model="sex" placeholder="请选择" style="width: 100%;">
				<el-option v-for="one in stateArr" :key="one.value" :label="one.label" :value="one.value"></el-option>
			</el-select>
		</el-form-item>        
		
		<el-form-item label="年龄">
			<el-select v-model="age" placeholder="请选择" style="width: 100%;">
				<el-option v-for="one in ageArr" :key="one" :label="one" :value="one"></el-option>
			</el-select>
		</el-form-item>
    </el-form>
    <span slot="footer" class="dialog-footer">
                <!--请修改这两行注释中间的代码来产生相应按钮的点击事件-->
                <el-button v-on:click="withdraw">一键撤销</el-button>
                <el-button type="primary"
                            v-on:click="ensure"
                            :disabled="state.username_valid===false"
                            >开始实验</el-button>
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
      age:"",
      sex:"",
      user:this.state.username,
      stateArr:[
        {value:'male',label:'男'},
		{vlaue:'female',label:'女'}
      ],
      ageArr:[]
    }
  },
  created(){
	this.ageArr = new Array(50).fill(10).map((el,i)=>10+i);
  },
  methods: {
    ensure:function(event){
      if(event && this.state.username_valid)
      {
        this.dialogVisible=false
        this.$emit('newMember',
        {age: this.age,
         sex: this.sex,
        user: this.state.username})
      }
    },
    withdraw:function(event){
      if(event)
        //this.dialogVisible=false
        //this.$emit('WITHDRAW')
        this.age="";
        this.sex="";
		this.state.username="";
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
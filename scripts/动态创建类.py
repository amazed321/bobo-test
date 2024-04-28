# class LevelModelForm(BootStrapForm, forms.ModelForm):
#     class Meta:
#         model = models.Level
#         fields = ["title", "percent"]

# ######### 案例1 #########
"""
# 基于定义实现
class LevelModelForm(object):
    name = "武沛齐"
    age = 19

    def func(self):
        return 123


# 基于创建类
LevelModelForm2 = type("LevelModelForm2", (object,), {"name": "武沛齐", "age": 19, "func": lambda self: 123})

obj = LevelModelForm2()
res = obj.func()
print(res)
"""

# ######### 案例2 #########
meta_cls = type("Meta", (object,), {"model": 123, "fields": [1122]})
model_form_cls = type("LevelModelForm", (BootStrapForm, forms.ModelForm), {"Meta": meta_cls})


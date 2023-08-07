from nacos.api.base import BaseNacosAPI


class NacosConfig(BaseNacosAPI):

    def get(self,
            group: str,
            dataId: str,
            *,
            namespace_id: str = 'public',
            tag: str = ''):
        """获取指定配置

        Parameters
        ----------
        group
            配置分组名
        dataId
            配置名
        namespace_id, optional
            命名空间, by default 'public'
        tag, optional
            标签, by default ''

        Returns
        -------
            _description_
        """
        params = {
            'dataId': dataId,
            'group': group,
            'namespaceId': namespace_id,
            'tag': tag
        }
        res = self._get('/nacos/v2/cs/config', params=params)
        return res

    def create(self,
               group: str,
               data_id: str,
               content: str,
               *,
               namespace_id: str = 'public',
               tag: str = '',
               app_name: str = '',
               src_user: str = '',
               config_tags: str = '',
               desc: str = '',
               effect: str = '',
               type: str = '',
               use: str = '',
               schema: str = '',
               ):
        """发布指定配置
        当配置已存在时，则对配置进行更新

        Parameters
        ----------
        group
            配置组名
        data_id
            配置名
        content
            配置内容
        namespace_id, optional
            命名空间, by default 'public'
        tag, optional
            标签, by default ''
        app_name, optional
            应用名, by default ''
        src_user, optional
            源用户, by default ''
        config_tags, optional
            配置标签列表,可多个,逗号分隔, by default ''
        desc, optional
            配置描述, by default ''
        effect, optional
            by default ''
        type, optional
            配置类型, by default ''
        use, optional
            by default ''
        schema, optional
            by default ''
        """
        data = {
            'group': group,
            'dataId': data_id,
            'content': content,
            'namespaceId': namespace_id,
            'tag': tag,
            'configTags': config_tags,
            'desc': desc,
            'effect': effect,
            'type': type,
            'appName': app_name,
            'srcUser': src_user,
            'use': use,
            'schema': schema,
        }
        return self._post('/nacos/v2/cs/config', data=data)

    def delete(self,
               group: str,
               dataId: str,
               *,
               namespace_id: str = 'public',
               tag: str = ''):
        """删除指定配置

        Parameters
        ----------
        group
            配置分组名
        dataId
            配置名
        namespace_id, optional
            命名空间, by default 'public'
        tag, optional
            标签, by default ''

        """
        params = {
            'dataId': dataId,
            'group': group,
            'namespaceId': namespace_id,
            'tag': tag
        }
        return self._delete('/nacos/v2/cs/config', params=params)

    def get_history_list(self,
                         group: str,
                         dataId: str,
                         *,
                         namespace_id: str = 'public',
                         page: int = 1,
                         page_size: int = 100):
        """获取指定配置的历史版本列表

        Parameters
        ----------
        group
            配置分组名
        dataId
            配置名
        namespace_id, optional
            命名空间, by default 'public'
        page, optional
            当前页, by default 1
        page_size, optional
            页条目数, 最大为500, by default 100
        """
        params = {
            'group': group,
            'dataId': dataId,
            'namespaceId': namespace_id,
            'pageNo': page,
            'pageSize': page_size
        }
        return self._get('/nacos/v2/cs/history/list', params=params)

    def get_history(self,
                    group: str,
                    dataId: str,
                    nid: int,
                    *,
                    namespace_id: str = 'public'):
        """获取指定版本的历史配置

        Parameters
        ----------
        group
            配置分组名
        dataId
            配置名
        nid
            历史配置id
        namespace_id, optional
            命名空间, by default 'public'
        """
        params = {
            'group': group,
            'dataId': dataId,
            'nid': nid,
            'namespaceId': namespace_id
        }
        return self._get('/nacos/v2/cs/history', params=params)

    def get_history_previous(self,
                             group: str,
                             dataId: str,
                             id: int,
                             *,
                             namespace_id: str = 'public'):
        """获取指定版本的历史配置

        Parameters
        ----------
        group
            配置分组名
        dataId
            配置名
        nid
            历史配置id
        namespace_id, optional
            命名空间, by default 'public'
        """
        params = {
            'group': group,
            'dataId': dataId,
            'id': id,
            'namespaceId': namespace_id
        }
        return self._get('/nacos/v2/cs/history/previous', params=params)

    def get_by_namespace(self, namespace_id: str):
        """获取指定命名空间下的配置信息列表

        Parameters
        ----------
        namespace_id
            命名空间
        """
        return self._get('/nacos/v2/cs/history/configs', params={'namespaceId': namespace_id})

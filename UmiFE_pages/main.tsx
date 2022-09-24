import {Button, message, Modal, Space} from 'antd'
import {CameraOutlined, LogoutOutlined, ScanOutlined} from '@ant-design/icons'
import styles from './main.less'
import {useEffect} from 'react'
import {history} from '@@/exports'
import axios from 'axios'

export default function Main() {
  useEffect(() => {
    // 判断用户是否有存储token
    const token = localStorage.getItem('token')
    if (token) return
    // 用户没有存储token
    message.error('请重新登录')
    history.push('/login')
  }, [])

  return (
    <div className={styles.box}>
      <div>
        <Space>
          <Button type="primary" icon={<CameraOutlined/>}>
            打开摄像头
          </Button>
          <Button icon={<ScanOutlined/>}>
            截图
          </Button>
          <Button danger icon={<LogoutOutlined/>} onClick={() => {
            Modal.confirm({
              title: '提醒',
              content: '是否要退出登录？',
              okText: '是',
              cancelText: '否',
              onOk: () => {
                // 弹框提示正在退出登录中...
                const hide = message.loading('正在退出登录中....', 0)

                // 发送请求给服务器：告知我们要退出登录
                axios
                  .post('http://127.0.0.1:5000/logout', null, {
                    headers: {
                      'Token': localStorage.getItem('token') + ''
                    }
                  })
                  .then(() => {
                    // 隐藏弹框
                    hide()

                    // 清除token
                    localStorage.removeItem('token')

                    // 打开登录界面
                    history.push('/login')
                  })
                  .catch(() => {
                    // 隐藏弹框
                    hide()

                    // 提示
                    message.error('退出登录失败')
                  })
              }
            })
          }}>
            退出登录
          </Button>
        </Space>
      </div>
      <div className={styles.content}>
        <video className={styles.video} src=""></video>
      </div>
    </div>
  )
}
import {React, useEffect} from 'react';
import Header from '../Components/HeaderComponent'
import { Upload, message } from 'antd';
import { UploadOutlined } from '@ant-design/icons';
import './MAM.css'
import {Link} from "react-router-dom";
import { Button } from 'antd';
import { Layout } from 'antd';
import { Typography } from 'antd';
import { Input } from 'antd';
import Footer from '../Components/Footer';
import Aos from "aos";



const { Title } = Typography;
const { Search } = Input;

const props = {
    name: 'file',
    action: 'https://www.mocky.io/v2/5cc8019d300000980a055e76',
    headers: {
      authorization: 'authorization-text',
    },
    onChange(info) {
      if (info.file.status !== 'uploading') {
        console.log(info.file, info.fileList);
      }
      if (info.file.status === 'done') {
        localStorage.setItem("picmam", info.file.name);
    } else if (info.file.status === 'error') {
        localStorage.setItem("picmam", info.file.name);
      }
    },
  };

function sendMaleDataMam(){
    localStorage.setItem("genderMAM", "M");
}
function sendFemaleDataMam(){
  localStorage.setItem("genderMAM", "F");
}

function MAM() {
    useEffect(()=>{
        Aos.init({duration: 500});
      },[]);

    return (
            <div>
            <Header/>
                <div className="container-upper">
                    <div className="overlay">
                        <div className="container-upper-content">
                            <p className="feature-heading">Make a match</p>
                            <div className="searchpanel__container">
                        <div data-aos="fade-right" className="searchPanel">
                            <p className="card-title">For Men</p>
                            <p>Upload the product you want to make a match with</p>

                            <div className="btn__container">
                            <Upload {...props}>  
                                    <div className="upload__mam">
                                        <Button icon={<UploadOutlined />}>Upload</Button>
                                    </div>
                                </Upload>
                                <Link to="/MAM/MAMRes">
                                    <Button onClick={sendMaleDataMam} className="search__mam">Search</Button>
                                </Link>
                            </div>       
                        </div>

                            <div data-aos="fade-left" className="searchPanel">
                            <p className="card-title">For Women</p>
                            <p>Upload the product you want to make a match with</p>
                                <Upload {...props}>  
                                    <div className="upload__mam">
                                        <Button icon={<UploadOutlined />}>Upload</Button>
                                    </div>
                                </Upload>
                                <Link to="/MAM/MAMRes">
                                    <Button onClick={sendFemaleDataMam} className="search__mam">Search</Button>
                                </Link>
                            </div>
                        </div>       
                                                          
                        </div>
                    </div>
                </div>
                <div data-aos="fade-up">
                <Footer/>
                </div>
                
            </div>
    );
}

export default MAM;
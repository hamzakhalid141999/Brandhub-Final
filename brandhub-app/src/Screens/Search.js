import React, {useState, useEffect} from 'react';
import Header from "../Components/HeaderComponent";
import "./Search.css";
import { Button } from 'antd';
import { Input } from 'antd';
import {Link} from "react-router-dom";
import { Upload, message } from 'antd';
import { UploadOutlined } from '@ant-design/icons';
import Aos from "aos";
import Footer from "../Components/Footer"




const { Search } = Input;

const onSearch = value => console.log(value);

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
        console.log(info.file.name);
        localStorage.setItem("inputPic", info.file.name);
    } else if (info.file.status === 'error') {
        console.log(info.file.name);
        localStorage.setItem("inputPic", info.file.name);
      }
    },
  };

function SearchComponent() {

    useEffect(()=>{
        Aos.init({duration: 500});
      },[]);

    const [inputString, setInputString] = useState(null)
    const [inputPic, setInputPic] = useState(null)

    function getData(val){
        setInputString(val.target.value)
    }
    function getPic(val){
        setInputPic(val.target.value)
    }
    function sendPicDataMale(){
        localStorage.setItem("sbiGender","M");
        var rangebtn = document.getElementById("range");
        var range = rangebtn.value;
        localStorage.setItem("range", range);
    }
    function sendPicDataFemale(){
        localStorage.setItem("sbiGender","F");
        var rangebtn = document.getElementById("range2");
        var range = rangebtn.value;
        localStorage.setItem("range", range);
    }
    function sendDataMale(){
        console.log(inputString);
        localStorage.setItem("inputString", inputString);
        localStorage.setItem("gender", "M");
        var rangebtn = document.getElementById("range");
        var range = rangebtn.value;
        localStorage.setItem("range", range);
    }
    function sendDataFemale(){
        console.log(inputString);
        localStorage.setItem("inputString", inputString);
        localStorage.setItem("gender", "F");        
        var rangebtn = document.getElementById("range2");
        var range = rangebtn.value;
        localStorage.setItem("range", range);
    }
    
    return (
        <div className="SearchComponent">
            <Header/>

            <div className="container-upper">
                <div className="overlay">
                    <div className="container-upper-content">
                        <p data-aos="fade-down" className="feature-heading">Search Like a Pro</p>

                        <div className="searchpanel__container">
                        <div style={{height: "390px"}} data-aos="fade-right" className="searchPanel">
                            <p className="card-title">For Men</p>
                                <p>Search by Text</p>

                                <div className="sbt__container">
                                    <Input placeholder="Search" onChange={getData}/>
                                    <div className="search">
                                        <Link to="/Search/SBTRes">
                                            <Button onClick={sendDataMale} type="primary" htmlType="submit">Search</Button>
                                        </Link>
                                    </div>
                                </div>     
                                

                                <p>Search By Image</p>
                                
                                <div className="sbi__btns">
                                    <div className="upload__btn">
                                        <Upload {...props}>  
                                            <div className="upload">
                                            <Button icon={<UploadOutlined />}>Upload</Button>
                                            </div>
                                        </Upload>
                                    </div>
                                    <div className="sbi__search">
                                        <Link to="/Search/SBIRes">
                                        <div className="searchImage">
                                            <Button onClick={sendPicDataMale} type="primary">Search</Button>
                                        </div>
                                        </Link>
                                    </div>
                               
                                </div>
                                
                                <br/>

                                <div className="horizontal-line"></div>

                                <select id="range" className="rangebtn">
                                    <option>Select Price Range</option>
                                    <option value="no">No filter</option>
                                    <option value=">=1000">Rs.1,000-Rs.2,000</option>
                                    <option value=">=2000">Rs.2,000-Rs.3,000</option>
                                    <option value=">=3000">Rs.3,000-Rs.4,000</option>
                                    <option value=">=4000">4000 above</option>
                                </select>

                                


                            </div>

                            <div style={{height: "390px"}} data-aos="fade-left" className="searchPanel">
                            <p className="card-title">For Women</p>
                                <p>Search by Text</p>

                                <div className="sbt__container">
                                    <Input placeholder="Search" onChange={getData}/>
                                    <div className="search">
                                        <Link to="/Search/SBTRes">
                                            <Button onClick={sendDataFemale} type="primary" htmlType="submit">Search</Button>
                                        </Link>
                                    </div>
                                </div>     
                                

                                <p>Search By Image</p>
                                
                                <div className="sbi__btns">
                                    <div className="upload__btn">
                                        <Upload {...props}>  
                                            <div className="upload">
                                            <Button icon={<UploadOutlined />}>Upload</Button>
                                            </div>
                                        </Upload>
                                    </div>
                                    <div className="sbi__search">
                                        <Link to="/Search/SBIRes">
                                        <div className="searchImage">
                                            <Button onClick={sendPicDataFemale} type="primary">Search</Button>
                                        </div>
                                        </Link>
                                    </div>
                               
                                </div>

                                <br/>

                                
                                <div className="horizontal-line"></div>

                                <select id="range2" className="rangebtn">
                                    <option>Select Price Range</option>
                                    <option value="no">No filter</option>
                                    <option value=">=1000">Rs.1,000-Rs.2,000</option>
                                    <option value=">=2000">Rs.2,000-Rs.3,000</option>
                                    <option value=">=3000">Rs.3,000-Rs.4,000</option>
                                    <option value=">=4000">4000 above</option>
                                </select>

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

export default SearchComponent;
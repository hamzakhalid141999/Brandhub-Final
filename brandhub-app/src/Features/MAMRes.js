import React, { Component } from 'react';
import './SBTRes.css'
import { Button } from 'antd';
import { Layout } from 'antd';
import { Typography } from 'antd';
import { Row, Col } from 'antd';
import { Breadcrumb } from 'antd';
import { UserOutlined, HomeOutlined, SearchOutlined } from '@ant-design/icons';
import { Link } from "react-router-dom";
import '../App.css';
import './SBTRes.css';
import './MAMRes.css';
import { Input } from 'antd';
import axios from 'axios'
import { Image } from 'antd';
import { Spin } from 'antd';
import Header from '../Components/HeaderComponent';


const { Title } = Typography;
const { Footer, Sider, Content } = Layout;
const { Search } = Input;

var load;
const api = axios.create({
  baseURL: 'http://127.0.0.1:5004'
})

const urlConvert = function (url) {
  var URLArray;
  var id;
  var newURL;
  URLArray = url.split('/');
  //console.log(URLArray[5]);
  id = URLArray[5];
  // console.log(id);
  newURL = "https://drive.google.com/thumbnail?id=" + id;
  console.log(newURL);
  return newURL;
}

class MAMRes extends Component {

  state = {
    products: [],
    matches: []
  }
  constructor() {
    super();

    load = 1;

    var inputGender = localStorage.getItem("genderMAM")
    console.log(inputGender);

    if (inputGender == 'M') {
      var apiURLMAM = '/mam/' + localStorage.getItem("picmam") + '/M';
      console.log(apiURLMAM);
    }
    else if (inputGender == 'F') {
      var apiURLMAM = '/mam/' + localStorage.getItem("picmam") + '/F';
      console.log(apiURLMAM);
    }

    api.get(apiURLMAM).then(res => {

      load = 0;

      for (let prod of Object.keys(res.data)) {
        console.log("Iteration")
        var prods = res.data[prod];
        console.table(res.data);

        if (res.data[1].Category == 'Top') {
          if (prods.Category == 'Top') {
            prods.ImageName[0] = urlConvert(prods.ImageName[0])
            this.setState({ products: [...this.state.products, prods] })
          }
          else if (prods.Category == 'Bottom') {
            prods.ImageName[0] = urlConvert(prods.ImageName[0])
            this.setState({ matches: [...this.state.matches, prods] })
          }
        }

        else if (res.data[1].Category == 'Bottom') {
          if (prods.Category == 'Bottom') {
            prods.ImageName[0] = urlConvert(prods.ImageName[0])
            this.setState({ products: [...this.state.products, prods] })
          }
          else if (prods.Category == 'Top') {
            prods.ImageName[0] = urlConvert(prods.ImageName[0])
            this.setState({ matches: [...this.state.matches, prods] })
          }
        }                                                       //object into the products list
      }
    })

  }
  render() {
    return (
      <div className="MAMRes">
          <Header/>
              <div className="container-breadcrumbs">
                <Breadcrumb separator=">">
                  <Breadcrumb.Item>
                    <UserOutlined />
                    <span><a>Login</a></span>
                  </Breadcrumb.Item>
                  <Breadcrumb.Item>
                    <HomeOutlined />
                    <span><Link to="/"><a>Dashboard</a></Link></span>
                  </Breadcrumb.Item>
                  <Breadcrumb.Item>
                    <SearchOutlined />
                    <span><Link to="/mam"><a>Make a match</a></Link></span>
                  </Breadcrumb.Item>
                  <Breadcrumb.Item>Search Results</Breadcrumb.Item>
                </Breadcrumb>
              </div>
              <Row>
                <Col span={24}>
                  <p className="pageHeading">The combinations we worked out!</p>
                </Col>
              </Row>

              <Row>

                <div className="matchitem__container">

                  {load == 1 ? <div className="loading"> <Spin style={{ marginLeft: "25px" }} size="large" /><h3>Please wait...</h3></div> :
                    this.state.products.map((products, index) =>
                      <Col span={4}>
                        <div className="matchpic_container">
                          <Image className="image"
                            src={products.ImageName[0]}
                            width={200}
                          />

                        </div>
                      </Col>
                    )

                  }

                </div>

              </Row>
              <Row style={{ marginTop: "70px" }}>
                <Col span={24}>
                  <p className="pageHeading">The matched products!</p>
                </Col>
              </Row>
              <Row>
                <div className="result__div">

                  {load == 1 ? <div className="loading"> <Spin style={{ marginLeft: "25px" }} size="large" /><h3>Please wait...</h3></div> : this.state.matches.map((match, index) =>
                    <div className="card">
                      <Image className="image__match" src={match.ImageName[0]} width={190} />
                      <div className="details__div">
                        <p className="prod__name">{match.PName}</p>
                        <p className="prod__price">{match.PPrice}</p>
                        <p className="prod__fabric">{match.Fabric}</p>
                        <p className="prod__color">{match.Color}</p>

                        <div className="openMatch">
                          <Button><a href={match.Link} target="blank">Open Product!</a></Button>
                        </div>
                      </div>

                    </div>
                  )}


                </div>
              </Row>
      </div>
    );
  }
}

export default MAMRes;
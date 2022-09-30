import React, { Component } from "react";
import { Routes, Route, useParams } from 'react-router-dom';
import { Grid, Button, Typography, Radio, FormControl, FormControlLabel, FormLabel, RadioGroup } from "@material-ui/core";
// import PosterImage from '../../static/images/ons_blanked.jpeg';

export default class Billboard extends Component {
  constructor(props) {
    super(props);

    this.state = {
      billboardId: parseInt(this.props.match.params.billboardId),
      questions: [],
    };

    this.getBillboardDetails = this.getBillboardDetails.bind(this);
    this.getBillboardDetails();
  }

  componentDidMount() {
    this.timer = setInterval(()=> this.getBillboardDetails(), 1000);
  }
  
  componentWillUnmount() {
    clearInterval(this.timer) 
    this.timer = null;
    // Fix the fact that this is not unmounting when we go to another page
  }

  getBillboardDetails() {
    return fetch("/api/get-billboard" + "?id=" + this.state.billboardId)
      .then((response) => {
        console.log(response)
        if (!response.ok) {
          console.log("Response not okay")
          this.props.history.push("/");
        }
        return response.json();
      })
      .then((data) => {
        console.log("Retrieved data from API")
        console.log(data)
        console.log(data.text) // program will probably crash here since we didnt send any text
        
        this.setState({
          name: data.name,
          text: data.text,
        });
      });
  }


  render() {
    return (
      <div>
        
        {/* <FormControl>
          <Grid container spacing={1}>
            
            <Grid item xs={12} align="center">
                Billboard ID: {this.state.billboardId}
                <br/>
                Billboard Text: {this.state.text}
                <br/>
            </Grid>

          </Grid>
        </FormControl> */}



        <div id="page-wrapper">
          <div id="overlay">
            <div id="major-text-section">
              {parseInt(this.state.text*10000)/100} %
            </div>

            <div id="minor-text-section">
              of people over 70 in QLD were 'chronically' lonely
            </div>
          </div>

          <img id="hero-image" src="../../static/images/ons_blanked.jpeg" alt="" />
          {/* <img id="hero-image" src={PosterImage} alt="" /> */}
        </div>

      </div>
    );
  }
}

import React from 'react';
import './Embedg.scss';
import Generator from "../components/embeds/Generator";
import Container from "react-bootstrap/Container";

function EmbedG() {
  return (
      <Container>
          <h1>Embed Generator</h1>
          <Generator/>
      </Container>
  );
}

export default EmbedG;

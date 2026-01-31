import React from 'react';
import { Heart, Globe, Users, Sparkles } from 'lucide-react';

const About = () => {
  return (
    <div className="bg-white">
      {/* Hero Section */}
      <section className="bg-brand-pink py-20 px-6 text-center">
        <h1 className="text-5xl font-serif text-gray-900 mb-6">Redefining Beauty</h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto leading-relaxed">
          We believe beauty is not about covering up, but about revealing the true radiance that lies within you.
        </p>
      </section>

      {/* Our Story */}
      <section className="max-w-7xl mx-auto px-6 py-20 grid md:grid-cols-2 gap-12 items-center">
        <div className="relative aspect-[4/5] bg-gray-100 rounded-2xl overflow-hidden">
          <img 
            src="https://images.unsplash.com/photo-1556228552-e934787dc83c?auto=format&fit=crop&q=80&w=800" 
            alt="Our Founder" 
            className="w-full h-full object-cover"
          />
        </div>
        <div className="space-y-6">
          <h2 className="text-3xl font-serif text-gray-900">Our Story</h2>
          <p className="text-gray-600 leading-relaxed">
            Founded in 2024, Bloom Beauty began with a simple question: Why must effective skincare be complicated? 
            Frustrated by 10-step routines and unpronounceable ingredients, we set out to create a line of products 
            that are as kind to the earth as they are to your skin.
          </p>
          <p className="text-gray-600 leading-relaxed">
            Every product we make is crafted with intention, using ethically sourced botanicals and clinical-grade 
            actives to deliver real results without the fluff.
          </p>
        </div>
      </section>

      {/* Values */}
      <section className="bg-gray-50 py-20">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-serif mb-4">Our Core Values</h2>
            <div className="w-24 h-1 bg-pink-600 mx-auto"></div>
          </div>
          
          <div className="grid md:grid-cols-4 gap-8">
            {[
              { icon: Heart, title: "Cruelty Free", desc: "We never test on animals, ever." },
              { icon: Globe, title: "Sustainable", desc: "Packaging made from recycled materials." },
              { icon: Users, title: "Inclusive", desc: "Formulated for all skin types and tones." },
              { icon: Sparkles, title: "Clean", desc: "No parabens, sulfates, or toxins." },
            ].map((item, idx) => (
              <div key={idx} className="bg-white p-8 rounded-xl shadow-sm hover:shadow-md transition text-center">
                <div className="text-pink-600 flex justify-center mb-4"><item.icon size={32} /></div>
                <h3 className="font-bold text-lg mb-2">{item.title}</h3>
                <p className="text-sm text-gray-500">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
};

export default About;